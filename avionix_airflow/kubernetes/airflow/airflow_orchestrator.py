from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.airflow.airflow_pods import AirflowDeployment
from avionix_airflow.kubernetes.airflow.airflow_roles import AirflowPodRoleGroup
from avionix_airflow.kubernetes.airflow.airflow_secrets import AirflowSecret
from avionix_airflow.kubernetes.airflow.airflow_service import (
    FlowerService,
    StatsDService,
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
from avionix_airflow.kubernetes.airflow.airflow_worker_pod_template import (
    PodTemplateWorkerConfig,
)
from avionix_airflow.kubernetes.airflow.dag_retrieval import DagRetrievalJob
from avionix_airflow.kubernetes.airflow.ingress_controller import AirflowIngress
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.monitoring.monitoring_options import MonitoringOptions
from avionix_airflow.kubernetes.orchestration import Orchestrator
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowOrchestrator(Orchestrator):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        values: ValueOrchestrator,
        airflow_options: AirflowOptions,
        monitoring_options: MonitoringOptions,
        cloud_options: CloudOptions,
    ):
        dag_group = AirflowDagVolumeGroup(airflow_options, cloud_options)
        log_group = AirflowLogVolumeGroup(airflow_options, cloud_options)
        external_volume_group = ExternalStorageVolumeGroup(
            airflow_options, cloud_options
        )
        components = [
            AirflowDeployment(
                sql_options,
                redis_options,
                airflow_options,
                monitoring_options,
                cloud_options,
            ),
            WebserverService(values, airflow_options.open_node_ports, cloud_options),
            dag_group.persistent_volume,
            log_group.persistent_volume,
            dag_group.persistent_volume_claim,
            log_group.persistent_volume_claim,
            external_volume_group.persistent_volume,
            external_volume_group.persistent_volume_claim,
            DagRetrievalJob(airflow_options, cloud_options),
            AirflowIngress(airflow_options, cloud_options),
            AirflowSecret(sql_options, airflow_options, redis_options),
            PodTemplateWorkerConfig(
                sql_options,
                redis_options,
                airflow_options,
                monitoring_options,
                cloud_options,
            ),
        ]
        if monitoring_options.enabled:
            components.append(StatsDService(values, airflow_options.open_node_ports))
        if airflow_options.in_celery_mode:
            components.append(
                FlowerService(values, airflow_options.open_node_ports, cloud_options)
            )
        if airflow_options.in_kube_mode:
            airflow_pod_service_account = AirflowPodServiceAccount()
            role_group = AirflowPodRoleGroup(airflow_pod_service_account)
            components.extend(
                [airflow_pod_service_account, role_group.role, role_group.role_binding]
            )
        super().__init__(components)
