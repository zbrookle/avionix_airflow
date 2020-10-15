from typing import Dict, Optional

from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class MasterNodeService(AirflowService):
    def __init__(
        self,
        name: str,
        port: int,
        node_port: int,
        values: ValueOrchestrator,
        node_ports_open: bool,
        port_name: str = "http",
        protocol: Optional[str] = None,
        service_type: str = "ClusterIP",
        annotations: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            name,
            port,
            port,
            node_port,
            values.master_node_labels,
            port_name=port_name,
            protocol=protocol,
            node_ports_open=node_ports_open,
            service_type=service_type,
            annotations=annotations,
        )


class FlowerService(MasterNodeService):
    __flower_port = 5555

    def __init__(
        self,
        values: ValueOrchestrator,
        node_ports_open: bool,
        cloud_options: CloudOptions,
    ):
        super().__init__(
            values.flower_service_name,
            self.__flower_port,
            values.flower_node_port,
            values,
            node_ports_open,
            values.flower_port_name,
            service_type=cloud_options.service_type,
        )
