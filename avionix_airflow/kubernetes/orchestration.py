from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from typing import List


class Orchestrator:
    _parts: List[KubernetesBaseObject] = []

    def __init__(self):
        self.parts = self._parts.copy()

    def get_kube_parts(self):
        return self.parts

    def __add__(self, other):
        if isinstance(other, Orchestrator):
            new_parts = self.parts + other.parts
            new_orchestrator = Orchestrator()
            new_orchestrator.parts = new_parts
            return new_orchestrator
