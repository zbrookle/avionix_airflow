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
        super().__init__(
            AirflowMeta(
                "airflow-ingress",
                annotations={"nginx.ingress.kubernetes.io/ssl-redirect": "false",},
            ),
            IngressSpec(
                backend=IngressBackend("default-http-backend", 80),
                rules=[
                    IngressRule(
                        HTTPIngressRuleValue(
                            [
                                HTTPIngressPath(
                                    IngressBackend(
                                        values.webserver_service_name,
                                        values.webserver_port_name,
                                    ),
                                    path="/airflow",
                                ),
                                HTTPIngressPath(
                                    IngressBackend(
                                        values.flower_service_name,
                                        values.flower_port_name,
                                    ),
                                    path="/flower",
                                ),
                            ]
                        ),
                        host=airflow_options.domain_name,
                    )
                ],
            ),
        )
