class MonitoringOptions:
    def __init__(
        self,
        enabled: bool = True,
        elastic_search_uri: str = "http://elasticsearch-master:9200",
    ):
        self.enabled = enabled
        self.elastic_search_uri = elastic_search_uri
