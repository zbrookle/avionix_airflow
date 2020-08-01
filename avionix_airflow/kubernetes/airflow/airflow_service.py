from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class MasterNodeService(AirflowService):
    def __init__(
        self,
        name: str,
        port: int,
        node_port: int,
        label: ValueOrchestrator,
        port_name: str = "http",
    ):
        super().__init__(
            name, port, port, node_port, label.master_node_labels, port_name=port_name
        )


class WebserverService(MasterNodeService):
    __webserver_port = 8080

    def __init__(self, values: ValueOrchestrator):
        super().__init__(
            values.webserver_service_name,
            self.__webserver_port,
            values.webserver_node_port,
            values,
            values.webserver_port_name,
        )


class FlowerService(MasterNodeService):
    __flower_port = 5555

    def __init__(self, values: ValueOrchestrator):
        super().__init__(
            values.flower_service_name,
            self.__flower_port,
            values.flower_node_port,
            values,
            values.flower_port_name,
        )


class StatsDService(MasterNodeService):
    __statsd_port = 8125

    def __init__(self, values: ValueOrchestrator):
        super().__init__(
            values.statsd_service_name,
            self.__statsd_port,
            values.statsd_node_port,
            values,
            values.statsd_port_name,
        )
