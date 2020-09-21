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
    AirflowSSHSecretsVolumeGroup,
    AirflowWorkerPodTemplateStorageGroup,
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

    def __repr__(self):
        return f"{type(self).__name__}({self.name} -> {self.value})"


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
    _command_entry_point: Optional[List[str]] = ["/entrypoint.sh"]

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
        self._name = name
        super().__init__(
            name=name,
            args=self._args,
            image="airflow-image"
            if airflow_options.local_mode
            else f"zachb1996/avionix_airflow:{self._airflow_options.master_image_tag}",
            image_pull_policy=airflow_options.image_pull_policy,
            env=self._get_environment(),
            env_from=[
                EnvFromSource(
                    secret_ref=SecretEnvSource(values.secret_name, optional=False)
                ),
            ],
            ports=ports,
            volume_mounts=self._get_volume_mounts(),
            readiness_probe=readiness_probe,
            command=self._command_entry_point,
        )

    def _get_volume_mounts(self):
        mounts = [
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
        if self._airflow_options.git_ssh_key:
            mounts.append(AirflowSSHSecretsVolumeGroup().volume_mount)
        return mounts

    def _get_environment(self):
        env = self._airflow_env + self._airflow_options.extra_env_vars
        if self._airflow_options.in_kube_mode:
            env += self._kubernetes_env
        if self._monitoring_options.enabled:
            env += self._elastic_search_env
        return env

    @property
    def _args(self) -> List[str]:
        return [self._name]

    @property
    def _executor(self):
        return self._airflow_options.core_executor

    @property
    def _airflow_env(self):
        return [
            CoreEnvVar("EXECUTOR", self._executor),
            CoreEnvVar("DEFAULT_TIMEZONE", self._airflow_options.default_timezone,),
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
            KubernetesEnvVar(
                "POD_TEMPLATE_FILE",
                "/usr/local/airflow/worker_pod_template/pod_template.yaml",
            ),
            KubernetesEnvVar(
                "DELETE_WORKER_PODS_ON_FAILURE",
                str(self._airflow_options.delete_pods_on_failure),
            ),
        ]
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


class AirflowWorker(AirflowContainer):
    _command_entry_point = None

    @property
    def _args(self):
        return []

    @property
    def _executor(self):
        """
        The executor for the worker pods must be local
        :return: LocalExecutor string
        """
        return "LocalExecutor"


class AirflowMasterContainer(AirflowContainer):
    def _get_volume_mounts(self):
        mounts = super()._get_volume_mounts()
        mounts.append(AirflowWorkerPodTemplateStorageGroup().volume_mount)
        return mounts


class WebserverUI(AirflowMasterContainer):
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


class Scheduler(AirflowMasterContainer):
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


class FlowerUI(AirflowMasterContainer):
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
