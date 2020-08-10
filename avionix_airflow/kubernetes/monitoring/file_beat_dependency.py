from avionix import ChartDependency
from avionix_airflow.kubernetes.monitoring.monitoring_options import MonitoringOptions
from yaml import dump


class FileBeatsContainerInput:
    def __init__(self, logs_path: str, index: str = ""):
        self.dict = {
            "type": "container",
            "paths": [f"{logs_path}/*.log"],
            "processors": [
                {
                    "add_kubernetes_metadata": {
                        "host": "${NODE_NAME}",
                        "matchers": [{"logs_path": {"logs_path": f"{logs_path}/"}}],
                    }
                }
            ],
        }
        if index:
            self.dict["index"] = "%{[agent.name]}-" + index + "%{+yyyy.MM.dd}"


class FileBeatDependency(ChartDependency):
    def __init__(self, monitoring_options: MonitoringOptions):
        self.__monitoring_options = monitoring_options
        super().__init__(
            "filebeat",
            "7.8.1",
            "https://helm.elastic.co",
            "elastic",
            values={
                "filebeatConfig": {
                    "filebeat.yml": dump(
                        {
                            "filebeat.inputs": [
                                FileBeatsContainerInput("/var/log/containers").dict,
                            ],
                            "output.elasticsearch": {
                                "host": "${NODE_NAME}",
                                "hosts": "${ELASTICSEARCH_HOSTS:%s}"
                                % self.__monitoring_options.elastic_search_uri,
                            },
                        }
                    )
                }
            },
        )
