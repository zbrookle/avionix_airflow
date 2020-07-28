from avionix import ObjectMeta
from avionix.kubernetes_objects.core import Namespace, NamespaceSpec

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions


class AirflowNamespace(Namespace):
    def __init__(self, airflow_options: AirflowOptions):
        super().__init__(ObjectMeta(name=airflow_options.namespace), NamespaceSpec())
