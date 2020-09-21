class ValueOrchestrator:
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

    @property
    def master_node_labels(self):
        return {"pod-job": "master-node"}

    @property
    def elasticsearch_proxy_labels(self):
        return {"pod-job": "es-proxy"}

    @property
    def database_labels(self):
        return {"pod-job": "database"}

    @property
    def redis_labels(self):
        return {"pod-job": "redis"}

    @property
    def dag_sync_cron_labels(self):
        return {"pod-job": "dag-sync"}

    @property
    def database_service_name(self):
        return "airflow-database-connection"

    @property
    def redis_service_name(self):
        return "redis-svc"

    @property
    def flower_service_name(self):
        return "flower-svc"

    @property
    def webserver_service_name(self):
        return "webserver-svc"

    @property
    def master_deployment_name(self):
        return "airflow-master-deployment"

    @property
    def database_deployment_name(self):
        return "postgres-database-deployment"

    @property
    def redis_deployment_name(self):
        return "redis-deployment"

    @property
    def webserver_port_name(self):
        return "webserver-port"

    @property
    def flower_port_name(self):
        return "flower-port"

    @property
    def webserver_node_port(self):
        return 30000

    @property
    def flower_node_port(self):
        return 30003

    @property
    def airflow_pod_service_account(self):
        return "airflow-pod-account"
