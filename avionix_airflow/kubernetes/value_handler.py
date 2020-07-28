class ValueOrchestrator:
    @property
    def master_node_labels(self):
        return {"pod-job": "master-node"}

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
    def webserver_node_port(self):
        return 8080

    @property
    def flower_node_port(self):
        return 30003
