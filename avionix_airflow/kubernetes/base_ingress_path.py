from avionix.kubernetes_objects.extensions import IngressBackend, HTTPIngressPath
from typing import Union


class AirflowIngressPath(HTTPIngressPath):
    def __init__(self, service_name: str, service_port: Union[int, str], path: str):
        super().__init__(IngressBackend(service_name, service_port), path=path)
