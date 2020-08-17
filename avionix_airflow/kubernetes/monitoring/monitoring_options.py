from avionix_airflow.kubernetes.value_handler import ValueOrchestrator

VIEW_MODES = ["Viewer", "Editor", "Admin"]
DEFAULT_ELASTIC_SEARCH_URI = "http://elasticsearch-master:9200"


class MonitoringOptions:
    """
    Configurations for monitoring airflow

    :param enabled: Whether or not monitoring should be enabled
    :param elastic_search_uri: The uri to use for elastic search
    :param grafana_role: The role to use for grafana can be one of \
        ["Viewer", "Editor", "Admin"]
    :param elastic_search_proxy_uri: The uri to use as the elastic search proxy, \
       this shouldn't be changed unless using an external elastic search provider
    """

    view_modes = VIEW_MODES

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
