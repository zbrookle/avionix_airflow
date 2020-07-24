from avionix_airflow.kubernetes.label_handler import LabelHandler
from avionix_airflow.kubernetes.base_service import AirflowService


class WebserverService(AirflowService):
    __webserver_port = 8080

    def __init__(self):
        label = LabelHandler()
        super().__init__(
            "webserver-connection",
            self.__webserver_port,
            self.__webserver_port,
            30000,
            label.master_node_labels,
            label.webserver_host,
            "http",
        )
