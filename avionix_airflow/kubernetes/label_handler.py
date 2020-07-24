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
        return "airflow-db"

    @property
    def webserver_host(self):
        return "airflow.webserver.com"
