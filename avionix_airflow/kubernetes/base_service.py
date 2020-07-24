from avionix.kubernetes_objects.service import Service, ServiceSpec, ServicePort
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from typing import Optional


class AirflowService(Service):
    def __init__(
        self,
        name: str,
        port: int,
        target_port: int,
        node_port: int,
        selector_labels: dict,
        external_name: Optional[str] = None,
        port_name: Optional[str] = None,
    ):
        super().__init__(
            AirflowMeta(name),
            ServiceSpec(
                [
                    ServicePort(
                        name=port_name,
                        port=port,
                        target_port=target_port,
                        node_port=node_port,
                    )
                ],
                selector=selector_labels,
                external_name=external_name,
                type="NodePort",
                external_traffic_policy="Local",
            ),
        )
