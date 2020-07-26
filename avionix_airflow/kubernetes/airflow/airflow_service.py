from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.kubernetes.label_handler import LabelHandler


class MasterNodeService(AirflowService):
    def __init__(self, name: str, port: int, node_port: int, label: LabelHandler):
        super().__init__(
            name, port, port, node_port, label.master_node_labels, port_name="http"
        )


class WebserverService(MasterNodeService):
    __webserver_port = 8080

    def __init__(self, label: LabelHandler):
        super().__init__(
            label.webserver_service_name, self.__webserver_port, 30000, label
        )


class FlowerService(MasterNodeService):
    __flower_port = 5555

    def __init__(self, label: LabelHandler):
        super().__init__(label.flower_service_name, self.__flower_port, 30003, label)
