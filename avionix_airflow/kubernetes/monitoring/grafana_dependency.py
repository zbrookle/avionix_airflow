from avionix import ChartDependency


class GrafanaDependency(ChartDependency):
    def __init__(self):
        super().__init__(
            "grafana",
            "5.5.2",
            "https://kubernetes-charts.storage.googleapis.com/",
            "stable",
            values={
                "datasources": {
                    "datasources.yaml": {
                        "apiVersion": 1,
                        "datasources": [
                            {
                                "default": True,
                                "name": "airflow",
                                "type": "elasticsearch",
                                "access": "proxy",
                                "database": "[airflow-]*",
                                "url": "http://elasticsearch-master:9200",
                                "jsonData": {
                                    "interval": "Daily",
                                    "esVersion": 70,
                                    "timeField": "@timestamp",
                                },
                            }
                        ],
                    }
                },
                "grafana.ini": {
                    "server": {
                        "domain": "www.avionix-airflow.com",
                        "root_url": "%(protocol)s://%(domain)s/grafana",
                        "serve_from_sub_path": True,
                    },
                    "auth.anonymous": {
                        "enabled": True,
                        "org_name": "Main Org.",
                        "org_role": "Admin",
                    },
                    "auth.basic": {"enabled": False},
                },
            },
        )
