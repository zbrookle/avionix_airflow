from typing import Optional

from avionix.kube.core import HTTPGetAction, Probe


class AvionixAirflowProbe(Probe):
    def __init__(self, path: str, port: int, host: Optional[str] = None):
        super().__init__(http_get=HTTPGetAction(path=path, port=port, host=host))
