from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AwsElasticSearchProxyService(AirflowService):
    def __init__(self):
        values = ValueOrchestrator()
        super().__init__(
            values.es_proxy_service_name,
            values.elasticsearch_proxy_port,
            values.elasticsearch_proxy_port,
            33000,
            values.elasticsearch_proxy_labels,
            port_name="https",
            protocol="TCP",
        )
