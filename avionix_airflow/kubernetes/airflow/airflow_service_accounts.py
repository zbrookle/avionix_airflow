from avionix.kube.core import ServiceAccount
from avionix.kube.meta import ObjectMeta

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowPodServiceAccount(ServiceAccount):
    def __init__(self, airflow_options: AirflowOptions):
        values = ValueOrchestrator()
        super().__init__(
            ObjectMeta(
                name=values.airflow_pod_service_account,
                namespace=airflow_options.namespace,
            )
        )
