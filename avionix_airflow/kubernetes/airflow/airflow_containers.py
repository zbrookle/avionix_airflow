from typing import List, Optional

from avionix.kubernetes_objects.core import (
    Container,
    ContainerPort,
    EnvVar,
    SecurityContext,
)

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.airflow.airflow_storage import (
    AirflowDagVolumeGroup,
    AirflowLogVolumeGroup,
)
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions


class AirflowContainer(Container):
    def __init__(
        self,
        name: str,
        args,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
        core_executor: str = "CeleryExecutor",
        ports: Optional[List[ContainerPort]] = None,
    ):
        self._sql_options = sql_options
        self._redis_options = redis_options
        super().__init__(
            name=name,
            args=args,
            image="airflow-image",
            image_pull_policy="Never",
            env=self._get_environment(core_executor),
            ports=ports,
            volume_mounts=[
                AirflowLogVolumeGroup(airflow_options).volume_mount,
                AirflowDagVolumeGroup(airflow_options).volume_mount,
            ],
        )

    def _get_environment(self, core_executor: str):
        env = self._sql_options.get_airflow_environment() + [
            EnvVar("AIRFLOW__CORE__EXECUTOR", core_executor)
        ]
        env.append(
            EnvVar(
                "AIRFLOW__CORE__SQL_ALCHEMY_CONN",
                self._sql_options.get_postgres_connection_string(),
            )
        )
        if core_executor == "CeleryExecutor":
            env.extend(
                [
                    EnvVar(
                        "AIRFLOW__CELERY__BROKER_URL",
                        self._redis_options.get_redis_connection_string(),
                    ),
                    EnvVar(
                        "AIRFLOW__CELERY__RESULT_BACKEND",
                        self._sql_options.get_postgres_connection_string(),
                    ),
                ]
            )
        return env


class WebserverUI(AirflowContainer):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
    ):
        super().__init__(
            "webserver",
            ["webserver"],
            sql_options,
            redis_options,
            airflow_options,
            ports=[ContainerPort(8080, host_port=8080)],
        )


class Scheduler(AirflowContainer):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
    ):
        super().__init__(
            "scheduler", ["scheduler"], sql_options, redis_options, airflow_options
        )


class FlowerUI(AirflowContainer):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
    ):
        super().__init__(
            "flower", ["flower"], sql_options, redis_options, airflow_options
        )
