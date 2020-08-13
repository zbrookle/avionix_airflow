from avionix import ChartDependency

from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.monitoring.monitoring_options import MonitoringOptions


class TelegrafDependency(ChartDependency):
    def __init__(
        self, monitoring_options: MonitoringOptions, cloud_options: CloudOptions
    ):
        super().__init__(
            "telegraf",
            "1.7.21",
            "https://helm.influxdata.com/",
            "influxdata",
            values={
                "replicaCount": 1,
                "env": [{"name": "HOSTNAME", "value": "telegraf"}],
                "service": {"enabled": True, "type": "ClusterIP", "annotations": {}},
                "serviceAccount": {"create": True},
                "config": {
                    "outputs": [
                        {
                            "elasticsearch": {
                                "urls": [monitoring_options.elastic_search_proxy_uri],
                                "timeout": "5s",
                                "health_check_interval": "10s",
                                "index_name": "airflow-%Y.%m.%d",
                                "manage_template": True,
                                "template_name": "airflow",
                                "overwrite_template": False,
                            },
                            "file": {
                                "files": ["stdout", "/tmp/metrics.out"],
                                "data_format": "json",
                                "json_timestamp_units": "1s",
                            },
                        }
                    ],
                    "inputs": [{"statsd": {"service_address": ":8125"}}],
                },
                "podAnnotations": cloud_options.elasticsearch_connection_annotations,
            },
        )
