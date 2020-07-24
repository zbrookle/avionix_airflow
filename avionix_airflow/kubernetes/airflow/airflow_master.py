from avionix.kubernetes_objects.deployment import Deployment, DeploymentSpec
from avionix.kubernetes_objects.pod import (
    PodTemplateSpec,
    PodSpec,
    LabelSelector,
)
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions
from avionix_airflow.kubernetes.airflow.airflow_containers import (
    WebserverUI,
    Scheduler,
    FlowerUI,
)
from avionix_airflow.kubernetes.label_handler import LabelHandler
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta


class AirflowPodTemplate(PodTemplateSpec):
    def __init__(self, sql_options: SqlOptions, redis_options: RedisOptions):
        super().__init__(
            AirflowMeta(
                name="airflow-master-pod", labels=LabelHandler().master_node_labels
            ),
            spec=PodSpec(
                [
                    WebserverUI(sql_options, redis_options),
                    Scheduler(sql_options, redis_options),
                    FlowerUI(sql_options, redis_options),
                ]
            ),
        )


class AirflowDeployment(Deployment):
    def __init__(self, sql_options: SqlOptions, redis_options: RedisOptions):
        super().__init__(
            AirflowMeta(name="airflow-master-deployment"),
            DeploymentSpec(
                AirflowPodTemplate(sql_options, redis_options),
                LabelSelector(LabelHandler().master_node_labels),
            ),
        )
