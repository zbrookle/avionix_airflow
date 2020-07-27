from avionix_airflow.kubernetes.airflow.airflow_master import AirflowDeployment
from avionix_airflow.kubernetes.airflow.airflow_namespace import AirflowNamespace
from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.airflow.airflow_service import (
    FlowerService,
    WebserverService,
)
from avionix_airflow.kubernetes.airflow.airflow_storage import (
    AirflowDagVolumeGroup,
    AirflowLogVolumeGroup,
)
from avionix_airflow.kubernetes.label_handler import LabelHandler
from avionix_airflow.kubernetes.orchestration import Orchestrator
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions


class AirflowOrchestrator(Orchestrator):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        label: LabelHandler,
        airflow_options: AirflowOptions,
    ):
        dag_group = AirflowDagVolumeGroup(airflow_options)
        log_group = AirflowLogVolumeGroup(airflow_options)
        super().__init__(
            [
                AirflowNamespace(),
                AirflowDeployment(sql_options, redis_options, airflow_options),
                WebserverService(label),
                FlowerService(label),
                dag_group.persistent_volume,
                log_group.persistent_volume,
                dag_group.persistent_volume_claim,
                log_group.persistent_volume_claim,
            ]
        )
