from pathlib import Path

from avionix import ChartDependency

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.monitoring.monitoring_options import MonitoringOptions
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions


class GrafanaDependency(ChartDependency):
    def __init__(
        self,
        monitoring_options: MonitoringOptions,
        airflow_options: AirflowOptions,
        sql_options: SqlOptions,
    ):
        self.__monitoring_options = monitoring_options
        self.__sql_options = sql_options
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
                            self.__elasticsearch_datasource,
                            self.__airflow_database_datasource,
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

    @property
    def __elasticsearch_datasource(self):
        return {
            "default": True,
            "name": "airflow",
            "type": "elasticsearch",
            "access": "proxy",
            "database": "[airflow-]*",
            "url": self.__monitoring_options.elastic_search_uri,
            "jsonData": {
                "interval": "Daily",
                "esVersion": 70,
                "timeField": "@timestamp",
            },
        }

    @property
    def __airflow_database_datasource(self):
        return {
            "default": False,
            "name": "Postgres",
            "type": "postgres",
            "url": f"{self.__sql_options.POSTGRES_HOST}:"
            f"{self.__sql_options.POSTGRES_PORT}",
            "database": self.__sql_options.POSTGRES_DB,
            "user": self.__sql_options.POSTGRES_USER,
            "secureJsonData": {"password": self.__sql_options.POSTGRES_PASSWORD},
            "jsonData": {"sslmode": "disable"},
        }
