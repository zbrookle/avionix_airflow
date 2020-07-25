from typing import List

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject


class Orchestrator:
    def __init__(self, parts: List[KubernetesBaseObject]):
        self.parts = parts

    def get_kube_parts(self):
        return self.parts

    def __add__(self, other):
        if isinstance(other, Orchestrator):
            return Orchestrator(self.parts + other.parts)
        raise self + other
