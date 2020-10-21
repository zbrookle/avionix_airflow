from typing import List

from avionix.kube.extensions import (
    HTTPIngressPath,
    HTTPIngressRuleValue,
    Ingress,
    IngressRule,
    IngressSpec,
)

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.base_ingress_path import AirflowIngressPath
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.services import ServiceFactory
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowIngress(Ingress):
    def __init__(
        self,
        airflow_options: AirflowOptions,
        cloud_options: CloudOptions,
        service_factory: ServiceFactory,
    ):
        values = ValueOrchestrator()
        ingress_paths: List[HTTPIngressPath] = cloud_options.extra_ingress_paths + [
            AirflowIngressPath(
                service_factory.webserver_service.metadata.name,
                service_factory.webserver_service.spec.ports[0].port,
                path="/airflow" + cloud_options.ingress_path_service_suffix,
            ),
            AirflowIngressPath(
                values.grafana_service_name,
                values.grafana_service_port,
                path="/grafana" + cloud_options.ingress_path_service_suffix,
            ),
        ]
        if airflow_options.in_celery_mode:
            ingress_paths.append(
                AirflowIngressPath(
                    service_factory.flower_service.metadata.name,
                    service_factory.flower_service.spec.ports[0].port,
                    path="/flower",
                )
            )
        super().__init__(
            AirflowMeta(
                "airflow-ingress", annotations=cloud_options.ingress_annotations
            ),
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
