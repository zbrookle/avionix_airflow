from avionix.kubernetes_objects.apps import Deployment, DeploymentSpec
from avionix.kubernetes_objects.meta import LabelSelector
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator
from avionix.kubernetes_objects.core import (
    PodTemplateSpec,
    PodSpec,
    Container,
    ContainerPort,
    Probe,
    HTTPGetAction,
)


class AwsElasticSearchProxyDeployment(Deployment):
    def __init__(self, cloud_options: CloudOptions, elastic_search_uri: str):
        values = ValueOrchestrator()

        probe = Probe(http_get=HTTPGetAction(path="/_cluster/health", port="https"))

        super().__init__(
            AirflowMeta(
                "aws-es-proxy",
            ),
            DeploymentSpec(
                replicas=1,
                selector=LabelSelector(values.elasticsearch_proxy_labels),
                template=PodTemplateSpec(
                    AirflowMeta(
                        "es-proxy",
                        labels=values.elasticsearch_proxy_labels,
                        annotations=cloud_options.elasticsearch_connection_annotations,
                    ),
                    spec=PodSpec(
                        [
                            Container(
                                "es-proxy",
                                image="abutaha/aws-es-proxy:latest",
                                image_pull_policy="IfNotPresent",
                                args=[
                                    "-listen",
                                    "0.0.0.0:9200",
                                    "-endpoint",
                                    elastic_search_uri,
                                    "-verbose"
                                ],
                                ports=[
                                    ContainerPort(9200, protocol="TCP", name="https")
                                ],
                                liveness_probe=probe,
                                readiness_probe=probe,
                            )
                        ]
                    ),
                ),
            ),
        )
