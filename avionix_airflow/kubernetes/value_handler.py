class ValueOrchestrator:
    _job_key = "pod-job"

    def __init__(self, dashboard_service_account: str = "dashboard"):
        self.dashboard_service_account = dashboard_service_account
        self.secret_name = "airflow-secrets"
        self.statsd_service_name = "statsd"
        self.statsd_node_port = 30004
        self.statsd_port_name = "statsd"
        self.elasticsearch_proxy_port = 9200
        self.es_proxy_service_name = "elasticsearch-master"
        self.grafana_service_name = "airflow-grafana"
        self.grafana_service_port = "service"
        self.airflow_worker_pod_template_config_file = "pod-template-config"
        self.master_node_labels = {self._job_key: "master-node"}
        self.worker_node_labels = {self._job_key: "worker-node"}
        self.database_labels = {self._job_key: "database"}
        self.redis_labels = {self._job_key: "redis"}
        self.dag_sync_cron_labels = {self._job_key: "dag-sync"}
        self.database_service_name = "airflow-database-connection"
        self.redis_service_name = "redis-svc"
        self.flower_service_name = "flower-svc"
        self.webserver_service_name = "webserver-svc"
        self.master_deployment_name = "airflow-master-deployment"
        self.database_deployment_name = "postgres-database-deployment"
        self.redis_deployment_name = "redis-deployment"
        self.webserver_port_name = "webserver-port"
        self.flower_port_name = "flower-port"
        self.webserver_node_port = 30000
        self.flower_node_port = 30003
        self.airflow_pod_service_account = "airflow-pod-account"

    @property
    def elasticsearch_proxy_labels(self):
        return {self._job_key: "es-proxy"}
