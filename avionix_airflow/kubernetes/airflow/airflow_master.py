from avionix.kubernetes_objects.apps import Deployment, DeploymentSpec
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
    ):
        log_volume_group = AirflowLogVolumeGroup(airflow_options)
        dag_volume_group = AirflowDagVolumeGroup(airflow_options)
        external_storage = ExternalStorageVolumeGroup(airflow_options)
        super().__init__(
            AirflowMeta(
                name="airflow-master-pod", labels=ValueOrchestrator().master_node_labels
            ),
            spec=PodSpec(
                [
                    WebserverUI(sql_options, redis_options, airflow_options),
                    Scheduler(sql_options, redis_options, airflow_options),
                    FlowerUI(sql_options, redis_options, airflow_options),
                ],
                volumes=[
                    log_volume_group.volume,
                    dag_volume_group.volume,
                    external_storage.volume,
                ],
            ),
        )


class AirflowDeployment(Deployment):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
    ):
        super().__init__(
            AirflowMeta(name="airflow-master-deployment"),
            DeploymentSpec(
                AirflowPodTemplate(sql_options, redis_options, airflow_options),
                LabelSelector(ValueOrchestrator().master_node_labels),
            ),
        )
