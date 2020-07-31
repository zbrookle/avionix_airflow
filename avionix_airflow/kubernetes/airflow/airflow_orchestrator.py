from avionix_airflow.kubernetes.airflow.airflow_master import AirflowDeployment
from avionix_airflow.kubernetes.airflow.airflow_namespace import AirflowNamespace
from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.airflow.airflow_roles import AirflowPodRoleGroup
from avionix_airflow.kubernetes.airflow.airflow_secrets import AirflowSecret
from avionix_airflow.kubernetes.airflow.airflow_service import (
    FlowerService,
    WebserverService,
)
from avionix_airflow.kubernetes.airflow.airflow_service_accounts import (
    AirflowPodServiceAccount,
)
from avionix_airflow.kubernetes.airflow.airflow_storage import (
    AirflowDagVolumeGroup,
    AirflowLogVolumeGroup,
    ExternalStorageVolumeGroup,
)
from avionix_airflow.kubernetes.airflow.dag_retrieval import DagRetrievalJob
from avionix_airflow.kubernetes.airflow.ingress_controller import AirflowIngress
from avionix_airflow.kubernetes.orchestration import Orchestrator
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowOrchestrator(Orchestrator):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        label: ValueOrchestrator,
        airflow_options: AirflowOptions,
    ):
        dag_group = AirflowDagVolumeGroup(airflow_options)
        log_group = AirflowLogVolumeGroup(airflow_options)
        external_volume_group = ExternalStorageVolumeGroup(airflow_options)
        components = [
            AirflowNamespace(airflow_options),
            AirflowDeployment(sql_options, redis_options, airflow_options),
            WebserverService(label),
            dag_group.persistent_volume,
            log_group.persistent_volume,
            dag_group.persistent_volume_claim,
            log_group.persistent_volume_claim,
            external_volume_group.persistent_volume,
            external_volume_group.persistent_volume_claim,
            DagRetrievalJob(airflow_options),
            AirflowIngress(airflow_options),
            AirflowSecret(sql_options, airflow_options, redis_options),
        ]
        if airflow_options.in_celery_mode:
            components.append(FlowerService(label))
        if airflow_options.in_kube_mode:
            airflow_pod_service_account = AirflowPodServiceAccount()
            role_group = AirflowPodRoleGroup(airflow_pod_service_account)
            components.extend(
                [airflow_pod_service_account, role_group.role, role_group.role_binding]
            )
        super().__init__(components)
