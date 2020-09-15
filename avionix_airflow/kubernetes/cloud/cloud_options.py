from abc import ABC, abstractmethod
from typing import Dict, List

from avionix import ChartDependency
from avionix.kube.base_objects import KubernetesBaseObject
from avionix.kube.core import CSIPersistentVolumeSource
from avionix.kube.extensions import IngressBackend
from avionix.kube.storage import StorageClass

from avionix_airflow.kubernetes.base_ingress_path import AirflowIngressPath


class CloudOptions(ABC):
    service_type = "LoadBalancer"
    preinstall_namepsace = "kube-system"
    ingress_path_service_suffix = ""

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
    def extra_ingress_paths(self) -> List[AirflowIngressPath]:
        pass

    @property
    @abstractmethod
    def default_backend(self) -> IngressBackend:
        pass

    @property
    @abstractmethod
    def elasticsearch_connection_annotations(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def get_elastic_search_proxy_elements(
        self, elastic_search_uri: str
    ) -> List[KubernetesBaseObject]:
        pass

    @property
    @abstractmethod
    def webserver_service_annotations(self) -> Dict[str, str]:
        return {}

    @property
    @abstractmethod
    def dag_retrieval_annotations(self) -> Dict[str, str]:
        return {}
