from avionix import ObjectMeta
from avionix.kubernetes_objects.core import CSIPersistentVolumeSource
from avionix.kubernetes_objects.storage import StorageClass

from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from typing import List
from avionix import ChartDependency


class AwsOptions(CloudOptions):
    def __init__(self, efs_id: str):
        self.__efs_id = efs_id
        super().__init__(
            StorageClass(
                ObjectMeta(name="efs-sc"), None, None, None, "efs.csi.aws.com", None
            ),
            "Filesystem",
        )

    def get_csi_persistent_volume_source(self, name: str):
        return CSIPersistentVolumeSource(
            driver="efs.csi.aws.com", volume_handle=f"{self.__efs_id}:/{name}",
        )

    def get_host_path_volume_source(self, host_path: str):
        return None

    def get_platform_dependent_kube_objects(self) -> List[KubernetesBaseObject]:
        return [self.storage_class]

    def get_cloud_dependencies(self) -> List[ChartDependency]:
        return [
            # TODO Put chart back in
            # ChartDependency(
            #     "aws-efs-csi-driver",
            #     "1.0.0",
            #     "https://kubernetes-sigs.github.io/aws-efs-csi-driver/",
            #     "aws-efs-csi-driver",
            # )
        ]
