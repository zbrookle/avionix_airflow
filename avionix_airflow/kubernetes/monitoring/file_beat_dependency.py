from avionix import ChartDependency


class FileBeatDependency(ChartDependency):
    def __init__(self):
        super().__init__(
            "filebeat",
            "7.8.1",
            "https://helm.elastic.co",
            "elastic",
            values={
                "filebeat.yml": {
                    "filebeat.inputs": [
                        {
                            "type": "container",
                            "paths": ["/var/log/containers/*.log"],
                            "processors": [
                                {
                                    "add_kubernetes_metadata": {
                                        "host": "${NODE_NAME}",
                                        "matchers": {
                                            "logs_path": {
                                                "logs_path": "/var/log/containers/"
                                            }
                                        },
                                    }
                                }
                            ],
                        },
                    ],
                    "output.elasticsearch": {
                        "host": "${NODE_NAME}",
                        "hosts": "${ELASTICSEARCH_HOSTS:elasticsearch-master:9200}",
                    },
                }
            },
        )
