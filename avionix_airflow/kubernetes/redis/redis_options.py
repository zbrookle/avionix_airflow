from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class RedisOptions:
    """
    Configuration for redis if using "CeleryExecutor" option in AirflowOptions

    :param port: The port to use for redis
    :param host: Name of the redis host, defaults to the internal service name
    :param proto: Redis protocol
    :param password: Redis password
    :param db_num: Redis db number
    """

    def __init__(
        self,
        port: int = 6379,
        host: str = ValueOrchestrator().redis_service_name,
        proto: str = "redis://",
        password: str = "",
        db_num: int = 1,
    ):
        self.port = port
        self.host = host
        self.proto = proto
        self.password = password
        self.db_num = db_num

    @property
    def redis_connection_string(self):
        prefix = f":{self.password}" if self.password else ""
        return f"{self.proto}{prefix}{self.host}:{self.port}/{self.db_num}"
