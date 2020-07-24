from avionix.kubernetes_objects.container import Container, ContainerPort
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions
from avionix.kubernetes_objects.env import EnvVar
from typing import List, Optional


class AirflowContainer(Container):
    def __init__(
        self,
        name: str,
        args,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
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
            env.append(
                EnvVar(
                    "AIRFLOW__CELERY__BROKER_URL",
                    self._redis_options.get_redis_connection_string(),
                )
            )
        return env


class WebserverUI(AirflowContainer):
    def __init__(self, sql_options: SqlOptions, redis_options: RedisOptions):
        super().__init__(
            "webserver",
            ["webserver"],
            sql_options,
            redis_options,
            ports=[ContainerPort(8080, host_port=8080)],
        )


class Scheduler(AirflowContainer):
    def __init__(self, sql_options: SqlOptions, redis_options: RedisOptions):
        super().__init__("scheduler", ["scheduler"], sql_options, redis_options)


class FlowerUI(AirflowContainer):
    def __init__(self, sql_options: SqlOptions, redis_options: RedisOptions):
        super().__init__("flower", ["flower"], sql_options, redis_options)
