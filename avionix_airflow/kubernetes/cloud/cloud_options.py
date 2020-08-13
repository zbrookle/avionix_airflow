from abc import ABC, abstractmethod
from typing import Dict, List

from avionix import ChartDependency
from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.core import CSIPersistentVolumeSource
from avionix.kubernetes_objects.extensions import IngressBackend
from avionix.kubernetes_objects.storage import StorageClass


class CloudOptions(ABC):
    service_type = "LoadBalancer"

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

    @property
    @abstractmethod
    def ingress_annotations(self) -> Dict[str, str]:
        pass

    @property
    @abstractmethod
    def default_backend(self) -> IngressBackend:
        pass

    @property
    @abstractmethod
    def elasticsearch_connection_annotations(self) -> Dict[str, str]:
        pass
