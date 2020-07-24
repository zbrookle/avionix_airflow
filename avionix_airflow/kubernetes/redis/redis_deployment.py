from avionix.kubernetes_objects.deployment import Deployment, DeploymentSpec
from avionix.kubernetes_objects.pod import PodTemplateSpec, PodSpec
from avionix.kubernetes_objects.selector import LabelSelector
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix.kubernetes_objects.container import Container
from avionix_airflow.kubernetes.label_handler import LabelHandler


class RedisPodTemplate(PodTemplateSpec):
    def __init__(self):
        labels = LabelHandler()
        super().__init__(
            AirflowMeta("redis-pod", labels=labels.redis_labels),
            PodSpec(
                [Container("redis", image="redis", image_pull_policy="IfNotPresent")],
            ),
        )


class RedisDeployment(Deployment):
    def __init__(self):
        labels = LabelHandler()
        super().__init__(
            AirflowMeta("redis-deployment"),
            DeploymentSpec(RedisPodTemplate(), LabelSelector(labels.redis_labels)),
        )
