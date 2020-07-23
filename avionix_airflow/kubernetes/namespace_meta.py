from avionix import ObjectMeta


class AirflowMeta(ObjectMeta):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name=name, namespace="airflow", *args, **kwargs)
