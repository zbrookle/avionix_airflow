from avionix.kubernetes_objects.deployment import Deployment, DeploymentSpec
from avionix.kubernetes_objects.pod import (
    PodTemplateSpec,
    PodSpec,
    Container,
    LabelSelector,
)
from avionix import ObjectMeta

master_labels = {"cluster-type": "master-node"}

class AirflowContainer(Container):
    def __init__(self, name, command):
        super().__init__(name=name, command=command, image="airflow-image")


class WebserverUI(AirflowContainer):
    def __init__(self):
        super().__init__(name="webserver", command=["webserver"])


class AirflowPodTemplate(PodTemplateSpec):
    def __init__(self):
        super().__init__(
            ObjectMeta(name="airflow-master-pod", labels=master_labels), spec=PodSpec([
                WebserverUI()])
        )


class AirflowDeployment(Deployment):
    def __init__(self):
        super().__init__(
            ObjectMeta(name="airflow-master-deployment", namespace="airflow"),
            DeploymentSpec(
                AirflowPodTemplate(), LabelSelector(master_labels)
            ),
        )
