from typing import Optional

from avionix import ObjectMeta


class AirflowMeta(ObjectMeta):
    def __init__(
        self,
        name: str,
        labels: Optional[dict] = None,
        annotations: Optional[dict] = None,
        namespace: Optional[str] = None,
    ):
        if labels is None:
            labels = {}
        else:
            labels = labels.copy()
        labels["app"] = "airflow"
        super().__init__(
            name=name, labels=labels, annotations=annotations, namespace=namespace
        )
