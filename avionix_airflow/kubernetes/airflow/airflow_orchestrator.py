from avionix.kube.core import Namespace
from avionix.kube.meta import ObjectMeta

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
from avionix_airflow.kubernetes.airflow.airflow_storage import StorageGroupFactory
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
        storage_group_factory = StorageGroupFactory(
            airflow_options, cloud_options, airflow_options.namespace
        )
        dag_group = storage_group_factory.dag_volume_group
        log_group = storage_group_factory.log_volume_group
        external_volume_group = storage_group_factory.external_storage_volume_group
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
            dag_group.pvc,
            log_group.pvc,
            external_volume_group.persistent_volume,
            external_volume_group.pvc,
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
            airflow_pod_service_account = AirflowPodServiceAccount(airflow_options)
            role_group = AirflowPodRoleGroup(
                airflow_pod_service_account, airflow_options
            )
            components.extend(
                [airflow_pod_service_account, role_group.role, role_group.role_binding]
            )
        if (
            airflow_options.pods_namespace != airflow_options.namespace
        ) and airflow_options.in_kube_mode:
            worker_storage_groups = StorageGroupFactory(
                airflow_options, cloud_options, airflow_options.pods_namespace
            )
            components.extend(
                [
                    Namespace(ObjectMeta(name=airflow_options.pods_namespace)),
                    worker_storage_groups.dag_volume_group.pvc,
                    worker_storage_groups.log_volume_group.pvc,
                    worker_storage_groups.external_storage_volume_group.pvc,
                ]
            )
        super().__init__(components)
