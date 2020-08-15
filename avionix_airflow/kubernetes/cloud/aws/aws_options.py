from typing import Dict, List, Optional

from avionix import ChartDependency, ObjectMeta
from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.core import CSIPersistentVolumeSource
from avionix.kubernetes_objects.extensions import IngressBackend
from avionix.kubernetes_objects.storage import StorageClass

from avionix_airflow.kubernetes.cloud.aws.elastic_search_proxy.proxy_deployment import (
    AwsElasticSearchProxyDeployment,
)
from avionix_airflow.kubernetes.cloud.aws.elastic_search_proxy.proxy_service import (
    AwsElasticSearchProxyService,
)
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions


class AwsOptions(CloudOptions):
    def __init__(
        self,
        efs_id: str,
        cluster_name: str,
        elastic_search_access_role_arn: str,
        default_role_arn: str,
        alb_role_arn: str,
        external_dns_role_arn: str,
        domain: str,
        domain_filters: Optional[List[str]] = None,
    ):
        self.__efs_id = efs_id
        self.__cluster_name = cluster_name
        self.__elastic_search_access_role = elastic_search_access_role_arn
        self.__default_role = default_role_arn
        self.__alb_role_arn = alb_role_arn
        self.__domain = domain
        self.__domain_filters = domain_filters
        self.__external_dns_role_arn = external_dns_role_arn
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
                    "rbac": {"create": True},
                    "podAnnotations": {"iam.amazonaws.com/role": self.__alb_role_arn},
                },
            ),
            ChartDependency(
                "kube2iam",
                "2.5.1",
                "https://kubernetes-charts.storage.googleapis.com/",
                "stable",
                values={
                    "extraArgs": {"default-role": self.__default_role},
                    "rbac": {"create": True},
                    "host": {"iptables": True, "interface": "eni+"},
                },
            ),
            ChartDependency(
                "external-dns",
                "3.3.0",
                "https://charts.bitnami.com/bitnami",
                "bitnami",
                values={
                    # "aws": {"zoneType": "private"},
                    "domainFilters": []
                    if self.__domain_filters is None
                    else self.__domain_filters,
                    "podAnnotations": {
                        "iam.amazonaws.com/role": self.__external_dns_role_arn
                    },
                },
            ),
        ]

    @property
    def ingress_annotations(self) -> Dict[str, str]:
        return {
            "kubernetes.io/ingress.class": "alb",
            "external-dns.alpha.kubernetes.io/hostname": self.__domain,
            "alb.ingress.kubernetes.io/target-type": "ip",
            "alb.ingress.kubernetes.io/scheme": "internal"
        }

    @property
    def default_backend(self) -> IngressBackend:
        return None

    @property
    def elasticsearch_connection_annotations(self) -> Dict[str, str]:
        return {"iam.amazonaws.com/role": self.__elastic_search_access_role}

    def get_elastic_search_proxy_elements(
        self, elastic_search_uri: str
    ) -> List[KubernetesBaseObject]:
        return [
            AwsElasticSearchProxyService(),
            AwsElasticSearchProxyDeployment(self, elastic_search_uri),
        ]

    @property
    def webserver_service_annotations(self) -> Dict[str, str]:
        return {
            "alb.ingress.kubernetes.io/healthcheck-path": "/airflow",
            "alb.ingress.kubernetes.io/successCodes": "200,308",
        }
