from pathlib import Path

from avionix import ChartDependency
from yaml import dump

from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.monitoring.monitoring_options import MonitoringOptions


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
                },
                {
                    "script": {
                        "lang": "javascript",
                        "id": "airflow_log_generator",
                        "source": self.js_event_code,
                    }
                },
            ],
        }
        if index:
            self.dict["index"] = "%{[agent.name]}-" + index + "%{+yyyy.MM.dd}"

    @property
    def js_event_code(self):
        with open(Path(__file__).parent / "event_js" / "event.js") as event_js:
            return event_js.read()


class FileBeatDependency(ChartDependency):
    def __init__(
        self, monitoring_options: MonitoringOptions, cloud_options: CloudOptions
    ):
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
                                "hosts": [
                                    self.__monitoring_options.elastic_search_proxy_uri
                                ],
                            },
                            "setup.ilm.enabled": False,
                        }
                    )
                },
                "podAnnotations": cloud_options.elasticsearch_connection_annotations,
                "image": "docker.elastic.co/beats/filebeat-oss",
            },
        )
