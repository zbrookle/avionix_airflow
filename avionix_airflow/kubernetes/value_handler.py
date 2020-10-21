from dataclasses import dataclass, field

_JOB_KEY = "pod-job"


# TODO Break apart into different application objects that contain, service,
#  deployment, etc.
@dataclass(frozen=True)
class ValueOrchestrator:
    dashboard_service_account: str = "dashboard"
    secret_name: str = "airflow-secrets"
    elasticsearch_proxy_port: int = 9200
    es_proxy_service_name: str = "elasticsearch-master"
    grafana_service_name: str = "airflow-grafana"
    grafana_service_port: str = "service"
    airflow_worker_pod_template_config_file: str = "pod-template-config"
    master_node_labels: dict = field(default_factory=lambda: {_JOB_KEY: "master-node"})
    worker_node_labels: dict = field(default_factory=lambda: {_JOB_KEY: "worker-node"})
    database_labels: dict = field(default_factory=lambda: {_JOB_KEY: "database"})
    redis_labels: dict = field(default_factory=lambda: {_JOB_KEY: "redis"})
    dag_sync_cron_labels: dict = field(default_factory=lambda: {_JOB_KEY: "dag-sync"})
    elasticsearch_proxy_labels: dict = field(
        default_factory=lambda: {_JOB_KEY: "es-proxy"}
    )
    redis_service_name: str = "redis-svc"
    master_deployment_name: str = "airflow-master-deployment"
    database_deployment_name: str = "postgres-database-deployment"
    redis_deployment_name: str = "redis-deployment"
    airflow_pod_service_account: str = "airflow-pod-account"
