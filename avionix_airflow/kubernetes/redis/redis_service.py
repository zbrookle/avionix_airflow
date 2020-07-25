from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.kubernetes.label_handler import LabelHandler
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions


class RedisService(AirflowService):
    def __init__(self, redis_options: RedisOptions):
        labels = LabelHandler()
        super().__init__(
            labels.redis_default_service_name,
            redis_options.port,
            redis_options.port,
            30002,
            selector_labels=labels.redis_labels,
        )
