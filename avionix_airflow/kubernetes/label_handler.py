class LabelHandler:
    @property
    def master_node_labels(self):
        return {"cluster-type": "master-node"}

    @property
    def database_labels(self):
        return {"cluster-type": "airflow-database"}

    @property
    def redis_labels(self):
        return {"cluster-type": "airflow-redis"}

    @property
    def database_service_name(self):
        return "airflow-database-connection"

    @property
    def redis_service_name(self):
        return "redis-connection"

    @property
    def flower_service_name(self):
        return "flower-connection"

    @property
    def webserver_service_name(self):
        return "webserver-connection"

    @property
    def master_deployment_name(self):
        return "airflow-master-deployment"

    @property
    def database_deployment_name(self):
        return "postgres-database-deployment"

    @property
    def redis_deployment_name(self):
        return "redis-deployment"
