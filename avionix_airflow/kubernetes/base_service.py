from typing import Dict, Optional

from avionix.kube.core import Service, ServicePort, ServiceSpec

from avionix_airflow.kubernetes.namespace_meta import AirflowMeta


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
        protocol: Optional[str] = None,
        node_ports_open: bool = False,
        service_type: str = "ClusterIP",
        annotations: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            AirflowMeta(name, annotations=annotations),
            ServiceSpec(
                [
                    ServicePort(
                        name=port_name,
                        port=port,
                        target_port=target_port,
                        node_port=node_port if node_ports_open else None,
                        protocol=protocol,
                    )
                ],
                selector=selector_labels,
                external_name=external_name,
                type="NodePort" if node_ports_open else service_type,
                external_traffic_policy="Local" if node_ports_open else None,
            ),
        )
