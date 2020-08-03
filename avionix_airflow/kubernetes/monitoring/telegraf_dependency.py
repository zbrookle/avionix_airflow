from avionix import ChartDependency


class TelegrafDependency(ChartDependency):
    def __init__(self):
        super().__init__(
            "telegraf",
            "1.7.21",
            "https://helm.influxdata.com/",
            "influxdata",
            values={
                "replicaCount": 1,
                "env": [{"name": "HOSTNAME", "value": "telegraf"}],
                "service": {"enabled": True, "type": "ClusterIP", "annotations": {},},
                "serviceAccount": {"create": True},
                "config": {
                    "outputs": [
                        {
                            "elasticsearch": {
                                "urls": ["http://elasticsearch-master:9200"],
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
            },
        )
