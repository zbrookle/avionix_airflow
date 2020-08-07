from typing import Optional

from avionix import ObjectMeta


class AirflowMeta(ObjectMeta):
    def __init__(self, name: str, labels: Optional[dict] = None, *args, **kwargs):
        if labels is None:
            labels = {}
        super().__init__(name=name, labels=labels, *args, **kwargs)
        self.labels["app"] = "airflow"
