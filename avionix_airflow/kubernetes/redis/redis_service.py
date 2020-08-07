from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class RedisService(AirflowService):
    def __init__(self, redis_options: RedisOptions):
        labels = ValueOrchestrator()
        super().__init__(
            labels.redis_service_name,
            redis_options.port,
            redis_options.port,
            30002,
            selector_labels=labels.redis_labels,
            node_ports_open=True,
        )
