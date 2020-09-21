from abc import ABC, abstractmethod
from typing import List

from avionix.kube.apps import (
    Deployment,
    DeploymentSpec,
    DeploymentStrategy,
    RollingUpdateDeployment,
)
from avionix.kube.core import PodSpec, PodTemplateSpec
from avionix.kube.meta import LabelSelector

from avionix_airflow.kubernetes.airflow.airflow_containers import (
    AirflowContainer,
    FlowerUI,
    Scheduler,
    WebserverUI,
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
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowPodTemplate(PodTemplateSpec, ABC):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
        monitoring_options: MonitoringOptions,
        cloud_options: CloudOptions,
        name: str,
        service_account: str = "default",
    ):
        values = ValueOrchestrator()
        self._sql_options = sql_options
        self._redis_options = redis_options
        self._airflow_options = airflow_options
        self._monitoring_options = monitoring_options
        self._cloud_options = cloud_options
        self._airflow_ssh_volume_group = AirflowSSHSecretsVolumeGroup()
        super().__init__(
            AirflowMeta(
                name=name,
                labels=values.master_node_labels,
                annotations=cloud_options.elasticsearch_connection_annotations,
            ),
            spec=PodSpec(
                self._get_containers(),
                volumes=self._volumes,
                service_account_name=service_account,
            ),
        )

    @property
    def _volumes(self):
        volumes = [
            AirflowLogVolumeGroup(self._airflow_options, self._cloud_options).volume,
            AirflowDagVolumeGroup(self._airflow_options, self._cloud_options).volume,
            ExternalStorageVolumeGroup(
                self._airflow_options, self._cloud_options
            ).volume,
        ]
        if self._airflow_options.git_ssh_key:
            volumes.append(self._airflow_ssh_volume_group.volume)
        return volumes

    @abstractmethod
    def _get_containers(self) -> List[AirflowContainer]:
        pass


class AirflowMasterPodTemplate(AirflowPodTemplate):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
        monitoring_options: MonitoringOptions,
        cloud_options: CloudOptions,
    ):
        service_account = (
            ValueOrchestrator().airflow_pod_service_account
            if airflow_options.in_kube_mode
            else None
        )
        self._worker_pod_template_storage_group = AirflowWorkerPodTemplateStorageGroup()
        super().__init__(
            sql_options,
            redis_options,
            airflow_options,
            monitoring_options,
            cloud_options,
            "airflow-master-pod",
            service_account,
        )

    def _get_containers(self):
        pods = [
            WebserverUI(
                self._sql_options,
                self._redis_options,
                self._airflow_options,
                self._monitoring_options,
                self._cloud_options,
            ),
            Scheduler(
                self._sql_options,
                self._redis_options,
                self._airflow_options,
                self._monitoring_options,
                self._cloud_options,
            ),
        ]
        if self._airflow_options.in_celery_mode:
            pods.append(
                FlowerUI(
                    self._sql_options,
                    self._redis_options,
                    self._airflow_options,
                    self._monitoring_options,
                    self._cloud_options,
                )
            )
        return pods

    @property
    def _volumes(self):
        volumes = super()._volumes
        volumes.append(self._worker_pod_template_storage_group.volume)
        return volumes


class AirflowDeployment(Deployment):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
        monitoring_options: MonitoringOptions,
        cloud_options: CloudOptions,
    ):
        super().__init__(
            AirflowMeta(name="airflow-master-deployment"),
            DeploymentSpec(
                AirflowMasterPodTemplate(
                    sql_options,
                    redis_options,
                    airflow_options,
                    monitoring_options,
                    cloud_options,
                ),
                LabelSelector(ValueOrchestrator().master_node_labels),
                strategy=DeploymentStrategy(
                    RollingUpdateDeployment(max_surge=1, max_unavailable=1)
                ),
            ),
        )
