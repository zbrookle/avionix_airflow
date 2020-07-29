from typing import List, Optional

from avionix.kubernetes_objects.core import (
    Container,
    ContainerPort,
    EnvVar,
    HTTPGetAction,
    Probe,
)

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.airflow.airflow_storage import (
    AirflowDagVolumeGroup,
    AirflowLogVolumeGroup,
    ExternalStorageVolumeGroup,
)
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions


class AirflowProbe(Probe):
    def __init__(self, path: str, port: int, host: str):
        super().__init__(http_get=HTTPGetAction(path=path, port=port, host=host))


class CoreEnvVar(EnvVar):
    def __init__(self, name: str, value):
        super().__init__("AIRFLOW__CORE__" + name, value)


class AirflowContainer(Container):
    def __init__(
        self,
        name: str,
        args,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
        ports: Optional[List[ContainerPort]] = None,
        readiness_probe: Optional[Probe] = None,
    ):
        self._sql_options = sql_options
        self._redis_options = redis_options
        self._airflow_options = airflow_options
        super().__init__(
            name=name,
            args=args,
            image="airflow-image",
            image_pull_policy="Never",
            env=self._get_environment(),
            ports=ports,
            volume_mounts=[
                AirflowLogVolumeGroup(airflow_options).volume_mount,
                AirflowDagVolumeGroup(airflow_options).volume_mount,
                ExternalStorageVolumeGroup(airflow_options).volume_mount,
            ],
            readiness_probe=readiness_probe,
        )

    def _get_environment(self):
        env = (
            self._sql_options.get_airflow_environment()
            + self._get_airflow_env()
            + self._get_celery_env()
            + self._get_kubernetes_env()
            + self._airflow_options.extra_env_vars
        )
        return env

    def _get_celery_env(self):
        return [
            EnvVar(
                "AIRFLOW__CELERY__BROKER_URL",
                self._redis_options.redis_connection_string,
            ),
            EnvVar(
                "AIRFLOW__CELERY__RESULT_BACKEND",
                self._sql_options.sql_alchemy_connection_string,
            ),
        ]

    def _get_airflow_env(self):
        return [
            CoreEnvVar("EXECUTOR", self._airflow_options.core_executor),
            CoreEnvVar(
                "SQL_ALCHEMY_CONN", self._sql_options.sql_alchemy_connection_string,
            ),
            EnvVar("AIRFLOW_CONN_POSTGRES_BACKEND", self._sql_options.sql_uri,),
            CoreEnvVar("DEFAULT_TIMEZONE", self._airflow_options.default_time_zone,),
            CoreEnvVar("LOAD_DEFAULT_CONNECTIONS", "False"),
            CoreEnvVar("FERNET_KEY", self._airflow_options.fernet_key),
        ]

    def _get_kubernetes_env(self):
        return [
            EnvVar("AIRFLOW__KUBERNETES__NAMESPACE", self._airflow_options.namespace)
        ]


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
            readiness_probe=AirflowProbe("/airflow", 8080, "0.0.0.0"),
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
            "flower",
            ["flower"],
            sql_options,
            redis_options,
            airflow_options,
            readiness_probe=Probe(http_get=HTTPGetAction("/flower/", 5555,)),
        )
