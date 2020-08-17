from avionix.kube.core import ServiceAccount

from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowPodServiceAccount(ServiceAccount):
    def __init__(self):
        values = ValueOrchestrator()
        super().__init__(AirflowMeta(values.airflow_pod_service_account))
