from avionix.kubernetes_objects.apps import Deployment, DeploymentSpec
from avionix.kubernetes_objects.core import (
    Container,
    ContainerPort,
    PodSpec,
    PodTemplateSpec,
)
from avionix.kubernetes_objects.meta import LabelSelector

from avionix_airflow.kubernetes.value_handler import ValueOrchestrator
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions


class RedisPodTemplate(PodTemplateSpec):
    def __init__(self, redis_options: RedisOptions):
        labels = ValueOrchestrator()
        super().__init__(
            AirflowMeta("redis-pod", labels=labels.redis_labels),
            PodSpec(
                [
                    Container(
                        "redis",
                        image="redis",
                        image_pull_policy="IfNotPresent",
                        ports=[ContainerPort(redis_options.port)],
                    )
                ],
            ),
        )


class RedisDeployment(Deployment):
    def __init__(self, redis_options: RedisOptions):
        labels = ValueOrchestrator()
        super().__init__(
            AirflowMeta("redis-deployment"),
            DeploymentSpec(
                RedisPodTemplate(redis_options), LabelSelector(labels.redis_labels)
            ),
        )
