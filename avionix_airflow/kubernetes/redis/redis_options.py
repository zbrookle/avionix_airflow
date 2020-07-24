from avionix_airflow.kubernetes.label_handler import LabelHandler


class RedisOptions:
    def __init__(
        self, port: int = 6379, host: str = LabelHandler().redis_default_service_name
    ):
        self.port = port
        self.host = host
