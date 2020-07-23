from avionix.kubernetes_objects.service import Service, ServiceSpec, ServicePort
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.label_handler import LabelHandler


class AirflowService(Service):
    def __init__(
        self, name: str, port: int, target_port: int, external_name: str, node_port:
            int
    ):
        label = LabelHandler()
        spec = ServiceSpec(
            [ServicePort(name="http", port=port, target_port=target_port,
                         node_port=node_port)],
            selector=label.master_node_labels,
            external_name=external_name,
            type="NodePort",
            external_traffic_policy="Local"
        )

        super().__init__(AirflowMeta(name), spec)


class WebserverService(AirflowService):
    def __init__(self):
        label = LabelHandler()
        super().__init__(
            "webserver-connection", 8080, 80, label.webserver_host, 30000
        )
