from typing import Dict, List

from avionix import ChartDependency, ObjectMeta
from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.core import CSIPersistentVolumeSource
from avionix.kubernetes_objects.extensions import IngressBackend
from avionix.kubernetes_objects.storage import StorageClass

from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions


class AwsOptions(CloudOptions):
    def __init__(self, efs_id: str, cluster_name: str, elastic_search_access_role: str):
        self.__efs_id = efs_id
        self.__cluster_name = cluster_name
        self.__elastic_search_access_role = elastic_search_access_role
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
            ChartDependency(
                "aws-alb-ingress-controller",
                "1.0.2",
                "https://kubernetes-charts-incubator.storage.googleapis.com",
                "incubator",
                values={
                    "clusterName": self.__cluster_name,
                    "autoDiscoverAwsRegion": True,
                    "autoDiscoverAwsVpcID": True,
                },
            ),
            ChartDependency(
                "kube2iam",
                "2.5.1",
                "https://kubernetes-charts.storage.googleapis.com/",
                "stable",
            ),
        ]

    @property
    def ingress_annotations(self) -> Dict[str, str]:
        return {"kubernetes.io/ingress.class": "alb"}

    @property
    def default_backend(self) -> IngressBackend:
        return None

    @property
    def elasticsearch_connection_annotations(self) -> Dict[str, str]:
        return {"iam.amazonaws.com/role": self.__elastic_search_access_role}
