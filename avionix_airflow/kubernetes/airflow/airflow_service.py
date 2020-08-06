from typing import Optional

from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class MasterNodeService(AirflowService):
    def __init__(
        self,
        name: str,
        port: int,
        node_port: int,
        label: ValueOrchestrator,
        test_mode: bool,
        port_name: str = "http",
        protocol: Optional[str] = None,
    ):
        super().__init__(
            name,
            port,
            port,
            node_port,
            label.master_node_labels,
            port_name=port_name,
            protocol=protocol,
            test_mode=test_mode,
        )


class WebserverService(MasterNodeService):
    __webserver_port = 8080

    def __init__(self, values: ValueOrchestrator, test_mode: bool):
        super().__init__(
            values.webserver_service_name,
            self.__webserver_port,
            values.webserver_node_port,
            values,
            test_mode,
            values.webserver_port_name,
        )


class FlowerService(MasterNodeService):
    __flower_port = 5555

    def __init__(self, values: ValueOrchestrator, test_mode: bool):
        super().__init__(
            values.flower_service_name,
            self.__flower_port,
            values.flower_node_port,
            values,
            test_mode,
            values.flower_port_name,
        )


class StatsDService(MasterNodeService):
    __statsd_port = 8125

    def __init__(self, values: ValueOrchestrator, test_mode: bool):
        super().__init__(
            values.statsd_service_name,
            self.__statsd_port,
            values.statsd_node_port,
            values,
            test_mode,
            values.statsd_port_name,
            protocol="UDP",
        )
