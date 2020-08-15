from avionix.kubernetes_objects.extensions import (
    HTTPIngressRuleValue,
    Ingress,
    IngressRule,
    IngressSpec,
)

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator
from avionix_airflow.kubernetes.base_ingress_path import AirflowIngressPath


class AirflowIngress(Ingress):
    def __init__(self, airflow_options: AirflowOptions, cloud_options: CloudOptions):
        values = ValueOrchestrator()
        ingress_paths = [
            AirflowIngressPath(
                values.webserver_service_name,
                values.webserver_port_name,
                path="/airflow",
            ),
            AirflowIngressPath(
                values.grafana_service_name,
                values.grafana_service_port,
                path="/grafana",
            ),
        ] + cloud_options.extra_ingress_paths
        if airflow_options.in_celery_mode:
            ingress_paths.append(
                AirflowIngressPath(
                    values.flower_service_name, values.flower_port_name, path="/flower"
                )
            )
        annotations = {"nginx.ingress.kubernetes.io/ssl-redirect": "false"}
        annotations.update(cloud_options.ingress_annotations)
        super().__init__(
            AirflowMeta("airflow-ingress", annotations=annotations),
            IngressSpec(
                backend=cloud_options.default_backend,
                rules=[
                    IngressRule(
                        HTTPIngressRuleValue(ingress_paths),
                        host=airflow_options.domain_name,
                    )
                ],
            ),
        )
