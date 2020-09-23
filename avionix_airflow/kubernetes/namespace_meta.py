from typing import Optional

from avionix import ObjectMeta


class AirflowMeta(ObjectMeta):
    def __init__(
        self,
        name: str,
        labels: Optional[dict] = None,
        annotations: Optional[dict] = None,
    ):
        if labels is None:
            labels = {}
        labels["app"] = "airflow"
        super().__init__(name=name, labels=labels, annotations=annotations)
