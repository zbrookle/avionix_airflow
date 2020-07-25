from avionix_airflow.kubernetes.orchestration import Orchestrator
from avionix_airflow.kubernetes.redis.redis_deployment import RedisDeployment
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions
from avionix_airflow.kubernetes.redis.redis_service import RedisService


class RedisOrchestrator(Orchestrator):
    def __init__(self, redis_options: RedisOptions):
        super().__init__([RedisDeployment(redis_options), RedisService(redis_options)])
