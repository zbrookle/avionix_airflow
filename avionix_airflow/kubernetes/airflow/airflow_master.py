from avionix.kubernetes_objects.deployment import Deployment, DeploymentSpec
from avionix.kubernetes_objects.pod import (
    PodTemplateSpec,
    PodSpec,
    LabelSelector,
)
from avionix import ObjectMeta
from kubernetes.airflow.airflow_containers import WebserverUI, Scheduler

master_labels = {"cluster-type": "master-node"}


class AirflowPodTemplate(PodTemplateSpec):
    def __init__(self):
        super().__init__(
            ObjectMeta(name="airflow-master-pod", labels=master_labels),
            spec=PodSpec([WebserverUI(), Scheduler()]),
        )


class AirflowDeployment(Deployment):
    def __init__(self):
        super().__init__(
            ObjectMeta(name="airflow-master-deployment", namespace="airflow"),
            DeploymentSpec(AirflowPodTemplate(), LabelSelector(master_labels)),
        )
