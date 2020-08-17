from typing import Union

from avionix.kube.extensions import HTTPIngressPath, IngressBackend


class AirflowIngressPath(HTTPIngressPath):
    def __init__(self, service_name: str, service_port: Union[int, str], path: str):
        super().__init__(IngressBackend(service_name, service_port), path=path)
