from typing import Optional

from avionix.kubernetes_objects.core import Service, ServicePort, ServiceSpec

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
        test_mode: bool = False,
    ):
        super().__init__(
            AirflowMeta(name),
            ServiceSpec(
                [
                    ServicePort(
                        name=port_name,
                        port=port,
                        target_port=target_port,
                        node_port=node_port if test_mode else None,
                        protocol=protocol,
                    )
                ],
                selector=selector_labels,
                external_name=external_name,
                type="NodePort" if test_mode else "ClusterIP",
                external_traffic_policy="Local" if test_mode else None,
            ),
        )
