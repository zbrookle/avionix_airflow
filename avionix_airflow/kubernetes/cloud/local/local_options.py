from typing import Dict, List

from avionix import ChartDependency, ObjectMeta
from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.core import (
    CSIPersistentVolumeSource,
    HostPathVolumeSource,
)
from avionix.kubernetes_objects.extensions import IngressBackend
from avionix.kubernetes_objects.storage import StorageClass

from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions


class LocalOptions(CloudOptions):
    service_type = "ClusterIP"

    def __init__(self):
        super().__init__(
            storage_class=StorageClass(
                ObjectMeta(name="standard"), None, None, None, "efs.csi.aws.com", None
            ),
            volume_mode="hostPath",
        )

    def get_csi_persistent_volume_source(self, name: str) -> CSIPersistentVolumeSource:
        return None

    def get_host_path_volume_source(self, host_path: str):
        return HostPathVolumeSource(host_path, type="DirectoryOrCreate")

    def get_cloud_dependencies(self) -> List[ChartDependency]:
        return []

    def get_platform_dependent_kube_objects(self) -> List[KubernetesBaseObject]:
        return []

    @property
    def ingress_annotations(self) -> Dict[str, str]:
        return {}

    @property
    def default_backend(self) -> IngressBackend:
        return IngressBackend("default-http-backend", 80)

    @property
    def elasticsearch_connection_annotations(self) -> Dict[str, str]:
        return {}

    def get_elastic_search_proxy_elements(
        self, elastic_search_uri: str
    ) -> List[KubernetesBaseObject]:
        return []
