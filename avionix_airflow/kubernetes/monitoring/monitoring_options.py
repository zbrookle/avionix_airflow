class MonitoringOptions:
    view_modes = ["Viewer", "Editor", "Admin"]

    def __init__(
        self,
        enabled: bool = True,
        elastic_search_uri: str = "http://elasticsearch-master:9200",
        grafana_role: str = "Viewer",
    ):
        if grafana_role not in self.view_modes:
            raise Exception(
                f"{grafana_role} is not a valid role, choose one of "
                f"{self.view_modes}"
            )
        self.enabled = enabled
        self.elastic_search_uri = elastic_search_uri
        self.grafana_role = grafana_role
