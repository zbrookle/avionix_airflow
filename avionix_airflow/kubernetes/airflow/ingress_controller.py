from avionix.kubernetes_objects.extensions import (
    HTTPIngressPath,
    HTTPIngressRuleValue,
    Ingress,
    IngressBackend,
    IngressRule,
    IngressSpec,
)

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowIngress(Ingress):
    def __init__(self, airflow_options: AirflowOptions):
        values = ValueOrchestrator()
        ingress_paths = [
            HTTPIngressPath(
                IngressBackend(
                    values.webserver_service_name, values.webserver_port_name,
                ),
                path="/airflow",
            ),
        ]
        if airflow_options.in_celery_mode:
            ingress_paths.append(
                HTTPIngressPath(
                    IngressBackend(
                        values.flower_service_name, values.flower_port_name,
                    ),
                    path="/flower",
                )
            )
        super().__init__(
            AirflowMeta(
                "airflow-ingress",
                annotations={"nginx.ingress.kubernetes.io/ssl-redirect": "false"},
            ),
            IngressSpec(
                backend=IngressBackend("default-http-backend", 80),
                rules=[
                    IngressRule(
                        HTTPIngressRuleValue(ingress_paths),
                        host=airflow_options.domain_name,
                    )
                ],
            ),
        )
