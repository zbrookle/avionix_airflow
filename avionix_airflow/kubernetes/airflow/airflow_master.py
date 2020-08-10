from avionix.kubernetes_objects.apps import (
    Deployment,
    DeploymentSpec,
    DeploymentStrategy,
    RollingUpdateDeployment,
)
from avionix.kubernetes_objects.core import PodSpec, PodTemplateSpec
from avionix.kubernetes_objects.meta import LabelSelector

from avionix_airflow.kubernetes.airflow.airflow_containers import (
    FlowerUI,
    Scheduler,
    WebserverUI,
)
from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.airflow.airflow_storage import (
    AirflowDagVolumeGroup,
    AirflowLogVolumeGroup,
    ExternalStorageVolumeGroup,
)
from avionix_airflow.kubernetes.monitoring.monitoring_options import MonitoringOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowPodTemplate(PodTemplateSpec):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
        monitoring_options: MonitoringOptions,
    ):
        log_volume_group = AirflowLogVolumeGroup(airflow_options)
        dag_volume_group = AirflowDagVolumeGroup(airflow_options)
        external_storage = ExternalStorageVolumeGroup(airflow_options)
        values = ValueOrchestrator()
        self.__sql_options = sql_options
        self.__redis_options = redis_options
        self.__airflow_options = airflow_options
        self.__monitoring_options = monitoring_options
        service_account = (
            values.airflow_pod_service_account if airflow_options.in_kube_mode else None
        )
        super().__init__(
            AirflowMeta(name="airflow-master-pod", labels=values.master_node_labels),
            spec=PodSpec(
                self.__get_containers(),
                volumes=[
                    log_volume_group.volume,
                    dag_volume_group.volume,
                    external_storage.volume,
                ],
                service_account_name=service_account,
            ),
        )

    def __get_containers(self):
        pods = [
            WebserverUI(
                self.__sql_options,
                self.__redis_options,
                self.__airflow_options,
                self.__monitoring_options,
            ),
            Scheduler(
                self.__sql_options,
                self.__redis_options,
                self.__airflow_options,
                self.__monitoring_options,
            ),
        ]
        if self.__airflow_options.in_celery_mode:
            pods.append(
                FlowerUI(
                    self.__sql_options,
                    self.__redis_options,
                    self.__airflow_options,
                    self.__monitoring_options,
                )
            )
        return pods


class AirflowDeployment(Deployment):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
        monitoring_options: MonitoringOptions,
    ):
        super().__init__(
            AirflowMeta(name="airflow-master-deployment"),
            DeploymentSpec(
                AirflowPodTemplate(
                    sql_options, redis_options, airflow_options, monitoring_options
                ),
                LabelSelector(ValueOrchestrator().master_node_labels),
                strategy=DeploymentStrategy(
                    RollingUpdateDeployment(max_surge=1, max_unavailable=1)
                ),
            ),
        )
