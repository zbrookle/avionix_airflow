from avionix_airflow.kubernetes.label_handler import LabelHandler
from avionix_airflow.kubernetes.base_service import AirflowService


class MasterNodeService(AirflowService):
    def __init__(self, name: str, port: int, node_port: int):
        label = LabelHandler()
        super().__init__(
            name, port, port, node_port, label.master_node_labels, port_name="http"
        )


class WebserverService(MasterNodeService):
    __webserver_port = 8080

    def __init__(self):
        super().__init__(
            "webserver-connection", self.__webserver_port, 30000,
        )


class FlowerService(MasterNodeService):
    __flower_port = 5555

    def __init__(self):
        super().__init__("flower-connection", self.__flower_port, 30003)
