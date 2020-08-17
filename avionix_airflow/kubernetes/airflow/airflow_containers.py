from typing import List, Optional

from avionix.kube.core import (
    Container,
    ContainerPort,
    EnvFromSource,
    EnvVar,
    Probe,
    SecretEnvSource,
)

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.airflow.airflow_storage import (
    AirflowDagVolumeGroup,
    AirflowLogVolumeGroup,
    ExternalStorageVolumeGroup,
)
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.monitoring.monitoring_options import MonitoringOptions
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.probes import AvionixAirflowProbe
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowEnvVar(EnvVar):
    def __init__(self, name: str, value):
        super().__init__("AIRFLOW__" + name, value)


class CoreEnvVar(AirflowEnvVar):
    def __init__(self, name: str, value):
        super().__init__("CORE__" + name, value)


class KubernetesEnvVar(AirflowEnvVar):
    def __init__(self, name: str, value):
        super().__init__("KUBERNETES__" + name, value)


class ElasticSearchEnvVar(AirflowEnvVar):
    def __init__(self, name: str, value):
        super().__init__("ELASTICSEARCH__" + name, value)


class KubernetesWorkerPodEnvVar(AirflowEnvVar):
    def __init__(self, name: str, value):
        super().__init__("KUBERNETES_ENVIRONMENT_VARIABLES__" + name, value)


class AirflowContainer(Container):
    def __init__(
        self,
        name: str,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
        monitoring_options: MonitoringOptions,
        cloud_options: CloudOptions,
        ports: Optional[List[ContainerPort]] = None,
        readiness_probe: Optional[Probe] = None,
    ):
        values = ValueOrchestrator()
        self._sql_options = sql_options
        self._redis_options = redis_options
        self._airflow_options = airflow_options
        self._monitoring_options = monitoring_options
        self._cloud_options = cloud_options
        super().__init__(
            name=name,
            args=[name],
            image="airflow-image"
            if airflow_options.local_mode
            else "zachb1996/avionix_airflow:latest",
            image_pull_policy="Never" if airflow_options.local_mode else "IfNotPresent",
            env=self._get_environment(),
            env_from=[
                EnvFromSource(
                    None, None, SecretEnvSource(values.secret_name, optional=False)
                )
            ],
            ports=ports,
            volume_mounts=self._get_volume_mounts(),
            readiness_probe=readiness_probe,
            command=["/entrypoint.sh"],
        )

    def _get_volume_mounts(self):
        return [
            AirflowLogVolumeGroup(
                self._airflow_options, self._cloud_options
            ).volume_mount,
            AirflowDagVolumeGroup(
                self._airflow_options, self._cloud_options
            ).volume_mount,
            ExternalStorageVolumeGroup(
                self._airflow_options, self._cloud_options
            ).volume_mount,
        ]

    def _get_environment(self):
        env = self._airflow_env + self._airflow_options.extra_env_vars
        if self._airflow_options.in_kube_mode:
            env += self._kubernetes_env
        if self._monitoring_options.enabled:
            env += self._elastic_search_env
        return env

    @property
    def _airflow_env(self):
        return [
            CoreEnvVar("EXECUTOR", self._airflow_options.core_executor),
            CoreEnvVar("DEFAULT_TIMEZONE", self._airflow_options.default_time_zone,),
            CoreEnvVar("LOAD_DEFAULT_CONNECTIONS", "False"),
            CoreEnvVar("LOAD_EXAMPLES", "False"),
            CoreEnvVar(
                "DAGS_ARE_PAUSED_AT_CREATION",
                str(self._airflow_options.dags_paused_at_creation),
            ),
            CoreEnvVar("REMOTE_LOGGING", str(self._monitoring_options.enabled)),
        ]

    @property
    def _elastic_search_env(self):
        return [
            ElasticSearchEnvVar(
                "HOST", self._monitoring_options.elastic_search_proxy_uri
            ),
            ElasticSearchEnvVar("WRITE_STDOUT", "True"),
            ElasticSearchEnvVar("JSON_FORMAT", "False"),
        ]

    @property
    def _kubernetes_env(self):
        kube_settings = [
            KubernetesEnvVar("NAMESPACE", self._airflow_options.namespace),
            KubernetesEnvVar(
                "DAGS_VOLUME_CLAIM",
                AirflowDagVolumeGroup(
                    self._airflow_options, self._cloud_options
                ).persistent_volume_claim.metadata.name,
            ),
            KubernetesEnvVar(
                "WORKER_CONTAINER_REPOSITORY", self._airflow_options.worker_image,
            ),
            KubernetesEnvVar("WORKER_CONTAINER_IMAGE_PULL_POLICY", "IfNotPresent",),
            KubernetesEnvVar(
                "WORKER_CONTAINER_TAG", self._airflow_options.worker_image_tag,
            ),
        ] + self._worker_pod_settings
        if not self._monitoring_options.enabled:
            kube_settings.append(
                KubernetesEnvVar(
                    "LOGS_VOLUME_CLAIM",
                    AirflowLogVolumeGroup(
                        self._airflow_options, self._cloud_options
                    ).persistent_volume_claim.metadata.name,
                )
            )
        return kube_settings

    @property
    def _worker_pod_settings(self):
        airflow_env = [var for var in self._airflow_env if "EXECUTOR" not in var.name]
        worker_env: List[AirflowEnvVar] = airflow_env + self._elastic_search_env
        return [KubernetesWorkerPodEnvVar(var.name, var.value) for var in worker_env]


class WebserverUI(AirflowContainer):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
        monitoring_options: MonitoringOptions,
        cloud_options: CloudOptions,
    ):
        super().__init__(
            "webserver",
            sql_options,
            redis_options,
            airflow_options,
            monitoring_options,
            cloud_options,
            ports=[ContainerPort(8080, host_port=8080)],
            readiness_probe=AvionixAirflowProbe("/airflow", 8080, "0.0.0.0"),
        )


class Scheduler(AirflowContainer):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
        monitoring_options: MonitoringOptions,
        cloud_options: CloudOptions,
    ):
        super().__init__(
            "scheduler",
            sql_options,
            redis_options,
            airflow_options,
            monitoring_options,
            cloud_options,
            [ContainerPort(8125, host_port=8125)],
        )


class FlowerUI(AirflowContainer):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
        monitoring_options: MonitoringOptions,
        cloud_options: CloudOptions,
    ):
        super().__init__(
            "flower",
            sql_options,
            redis_options,
            airflow_options,
            monitoring_options,
            cloud_options=cloud_options,
            readiness_probe=AvionixAirflowProbe("/flower/", 5555),
        )
