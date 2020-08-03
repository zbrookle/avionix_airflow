from avionix import ChartDependency
from avionix_airflow.kubernetes.monitoring.monitoring_options import MonitoringOptions
from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from pathlib import Path


class GrafanaDependency(ChartDependency):
    def __init__(
        self, monitoring_options: MonitoringOptions, airflow_options: AirflowOptions
    ):
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
                                "url": monitoring_options.elastic_search_uri,
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
                        "domain": airflow_options.domain_name,
                        "root_url": "%(protocol)s://%(domain)s/grafana",
                        "serve_from_sub_path": True,
                    },
                    "auth.anonymous": {
                        "enabled": True,
                        "org_name": "Main Org.",
                        "org_role": monitoring_options.grafana_role,
                    },
                    "auth.basic": {"enabled": False},
                },
                "dashboards": {
                    "default": {"airflow-dashboard": {"json": self.dashboard_json}}
                },
                "dashboardProviders": {
                    "dashboardproviders.yaml": {
                        "apiVersion": 1,
                        "providers": [
                            {
                                "name": "default",
                                "orgId": 1,
                                "folder": "",
                                "type": "file",
                                "disableDeletion": False,
                                "editable": True,
                                "options": {
                                    "path": "/var/lib/grafana/dashboards/default"
                                },
                            }
                        ],
                    }
                },
            },
        )

    @property
    def dashboard_json(self):
        with open(
            Path(__file__).parent / "dashboards" / "grafana_dashboard.json"
        ) as dashboard_file:
            return dashboard_file.read()
