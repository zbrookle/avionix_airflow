from abc import ABC, abstractmethod
from typing import List

from avionix import ChartDependency
from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.core import CSIPersistentVolumeSource
from avionix.kubernetes_objects.storage import StorageClass


class CloudOptions(ABC):
    def __init__(self, storage_class: StorageClass, volume_mode: str):
        self.storage_class = storage_class
        self.volume_mode = volume_mode

    @abstractmethod
    def get_csi_persistent_volume_source(self, name: str) -> CSIPersistentVolumeSource:
        pass

    @abstractmethod
    def get_host_path_volume_source(self, host_path: str):
        pass

    @abstractmethod
    def get_platform_dependent_kube_objects(self) -> List[KubernetesBaseObject]:
        pass

    @abstractmethod
    def get_cloud_dependencies(self) -> List[ChartDependency]:
        pass
