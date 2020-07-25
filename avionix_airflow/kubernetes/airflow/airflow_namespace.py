from avionix import ObjectMeta
from avionix.kubernetes_objects.core import Namespace, NamespaceSpec


class AirflowNamespace(Namespace):
    def __init__(self):
        super().__init__(ObjectMeta(name="airflow"), NamespaceSpec())
