from json import dumps
from typing import Dict, List, Optional

from avionix import ChartDependency, ObjectMeta
from avionix.kube.base_objects import KubernetesBaseObject
from avionix.kube.core import CSIPersistentVolumeSource
from avionix.kube.extensions import IngressBackend
from avionix.kube.storage import StorageClass

from avionix_airflow.kubernetes.base_ingress_path import AirflowIngressPath
from avionix_airflow.kubernetes.cloud.aws.elastic_search_proxy.proxy_deployment import (
    AwsElasticSearchProxyDeployment,
)
from avionix_airflow.kubernetes.cloud.aws.elastic_search_proxy.proxy_service import (
    AwsElasticSearchProxyService,
)
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AwsOptions(CloudOptions):
    """
    Settings for the AWS Managed Node Group setup

    :param efs_id: The id of the EFS file system to use as the storage provider
    :param cluster_name: The name of the EKS cluster
    :param elastic_search_access_role_arn: The IAM role arn for accessing elastic search
    :param default_role_arn: The default IAM role arn for pods in the cluster
    :param alb_role_arn: The IAM role setting up application load balancing
    :param external_dns_role_arn: The IAM role for setting the domain name
    :param autoscaling_role_arn: The IAM role for controlling the cluster scaling
    :param domain: The AWS domain name to use
    :param dag_sync_role_arn: The IAM role use for controlling retrieval of dags
    :param domain_filters: A list used to filter out route53 domain names
    :param use_ssl: Whether or not to use SSL encryption, (Recommended to be True)
    """

    _use_annotation = "use-annotation"
    _grafana_redirect = "grafana-redirect"
    _airflow_redirect = "airflow-redirect"
    ingress_path_service_suffix = "*"

    def __init__(
        self,
        efs_id: str,
        cluster_name: str,
        elastic_search_access_role_arn: str,
        default_role_arn: str,
        alb_role_arn: str,
        external_dns_role_arn: str,
        autoscaling_role_arn: str,
        dag_sync_role_arn: str,
        domain: str,
        domain_filters: Optional[List[str]] = None,
        use_ssl: bool = False,
    ):
        self.__efs_id = efs_id
        self.__cluster_name = cluster_name
        self.__elastic_search_access_role = elastic_search_access_role_arn
        self.__default_role = default_role_arn
        self.__alb_role_arn = alb_role_arn
        self.__domain = domain
        self.__domain_filters = domain_filters
        self.__external_dns_role_arn = external_dns_role_arn
        self.__values = ValueOrchestrator()
        self.__use_ssl = use_ssl
        self.__autoscaling_role_arn = autoscaling_role_arn
        self.__dag_sync_role_arn = dag_sync_role_arn
        super().__init__(
            StorageClass(ObjectMeta(name="efs-sc"), "efs.csi.aws.com"), "Filesystem",
        )

    def get_csi_persistent_volume_source(self, name: str):
        return CSIPersistentVolumeSource(
            driver="efs.csi.aws.com", volume_handle=f"{self.__efs_id}:/{name}"
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
                    "domainFilters": []
                    if self.__domain_filters is None
                    else self.__domain_filters,
                    "podAnnotations": {
                        "iam.amazonaws.com/role": self.__external_dns_role_arn
                    },
                },
            ),
            ChartDependency(
                "cluster-autoscaler",
                "7.3.4",
                "https://kubernetes-charts.storage.googleapis.com/",
                "stable",
                values={
                    "autoDiscovery": {"clusterName": "hmi-dev-team-cluster"},
                    "extraArgs": {"skip-nodes-with-system-pods": False},
                    "podAnnotations": {
                        "iam.amazonaws.com/role": self.__autoscaling_role_arn
                    },
                },
            ),
        ]

    @staticmethod
    def _get_wildcard_path_pattern(path: str):
        return dumps(
            [{"Field": "path-pattern", "PathPatternConfig": {"Values": [f"{path}*"]}}]
        )

    def _get_redirect(self, path: str, query: str = ""):
        redirect_config = {
            "Host": "#{host}",
            "Path": path,
            "Port": "80",
            "Protocol": "HTTP",
            "Query": query,
            "StatusCode": "HTTP_302",
        }
        if self.__use_ssl:
            redirect_config["Protocol"] = "HTTPS"
            redirect_config["Port"] = "443"
        redirect = {
            "Type": "redirect",
            "RedirectConfig": redirect_config,
        }

        return dumps(redirect)

    @property
    def ingress_annotations(self) -> Dict[str, str]:
        ingress_prefix = "alb.ingress.kubernetes.io"
        annotations = {
            "kubernetes.io/ingress.class": "alb",
            "external-dns.alpha.kubernetes.io/hostname": self.__domain,
            f"{ingress_prefix}/target-type": "ip",
            f"{ingress_prefix}/scheme": "internal",
            f"{ingress_prefix}/actions.{self._grafana_redirect}": self._get_redirect(
                "/grafana/", "orgid=1"
            ),
            f"{ingress_prefix}/actions.{self._airflow_redirect}": self._get_redirect(
                "/airflow/admin"
            ),
        }
        if self.__use_ssl:
            annotations[
                "alb.ingress.kubernetes.io/listen-ports"
            ] = '[{"HTTPS":443, "HTTP":80 }]'
            annotations["alb.ingress.kubernetes.io/actions.ssl-redirect"] = dumps(
                {
                    "Type": "redirect",
                    "RedirectConfig": {
                        "Protocol": "HTTPS",
                        "Port": "443",
                        "StatusCode": "HTTP_301",
                    },
                }
            )

        return annotations

    @property
    def extra_ingress_paths(self) -> List[AirflowIngressPath]:
        ingress_paths = [
            AirflowIngressPath(
                self._grafana_redirect, self._use_annotation, path="/grafana"
            ),
            AirflowIngressPath(
                self._airflow_redirect, self._use_annotation, path="/airflow"
            ),
        ]
        if self.__use_ssl:
            return [
                AirflowIngressPath("ssl-redirect", self._use_annotation, path="/*"),
            ] + ingress_paths
        return ingress_paths

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

    @property
    def dag_retrieval_annotations(self) -> Dict[str, str]:
        return {"iam.amazonaws.com/role": self.__dag_sync_role_arn}
