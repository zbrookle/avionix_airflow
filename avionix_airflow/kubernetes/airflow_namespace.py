from avionix.kubernetes_objects.namespace import Namespace, NamespaceSpec
from avionix import ObjectMeta


class AirflowNamespace(Namespace):
    def __init__(self):
        super().__init__(ObjectMeta(name="airflow"), NamespaceSpec())
