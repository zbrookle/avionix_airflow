from avionix.kubernetes_objects.deployment import Deployment, DeploymentSpec
from avionix.kubernetes_objects.pod import PodTemplateSpec, PodSpec
from avionix.kubernetes_objects.selector import LabelSelector
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix.kubernetes_objects.container import Container, ContainerPort
from avionix_airflow.kubernetes.label_handler import LabelHandler
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions


class RedisPodTemplate(PodTemplateSpec):
    def __init__(self, redis_options: RedisOptions):
        labels = LabelHandler()
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
        labels = LabelHandler()
        super().__init__(
            AirflowMeta("redis-deployment"),
            DeploymentSpec(
                RedisPodTemplate(redis_options), LabelSelector(labels.redis_labels)
            ),
        )
