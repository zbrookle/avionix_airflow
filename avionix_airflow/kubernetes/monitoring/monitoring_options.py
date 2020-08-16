DEFAULT_ELASTIC_SEARCH_URI = "http://elasticsearch-master:9200"
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class MonitoringOptions:
    view_modes = ["Viewer", "Editor", "Admin"]

    def __init__(
        self,
        enabled: bool = True,
        elastic_search_uri: str = DEFAULT_ELASTIC_SEARCH_URI,
        grafana_role: str = "Viewer",
        elastic_search_proxy_uri: str = ValueOrchestrator().es_proxy_service_name,
    ):
        if grafana_role not in self.view_modes:
            raise Exception(
                f"{grafana_role} is not a valid role, choose one of "
                f"{self.view_modes}"
            )
        self.enabled = enabled
        self.elastic_search_uri = elastic_search_uri
        self.grafana_role = grafana_role
        self.enable_elasticsearch_dependency = False
        if elastic_search_uri == DEFAULT_ELASTIC_SEARCH_URI:
            self.enable_elasticsearch_dependency = True
        self.elastic_search_proxy_uri = f"http://{elastic_search_proxy_uri}:9200"
