from typing import List

from avionix.kube.core import ConfigMap
from yaml import dump

from avionix_airflow.kubernetes.airflow.airflow_containers import (
    AirflowContainer,
    AirflowWorker,
)
from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.airflow.airflow_pods import AirflowPodTemplate
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.monitoring.monitoring_options import MonitoringOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.redis.redis_options import RedisOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowWorkerPodTemplate(AirflowPodTemplate):
    def _get_containers(self) -> List[AirflowContainer]:
        return [
            AirflowWorker(
                "base",
                self._sql_options,
                self._redis_options,
                self._airflow_options,
                self._monitoring_options,
                self._cloud_options,
            )
        ]


class PodTemplateWorkerConfig(ConfigMap):
    def __init__(
        self,
        sql_options: SqlOptions,
        redis_options: RedisOptions,
        airflow_options: AirflowOptions,
        monitoring_options: MonitoringOptions,
        cloud_options: CloudOptions,
    ):
        config_file = ValueOrchestrator().airflow_worker_pod_template_config_file
        super().__init__(
            AirflowMeta(config_file),
            data={
                config_file: dump(
                    AirflowWorkerPodTemplate(
                        sql_options,
                        redis_options,
                        airflow_options,
                        monitoring_options,
                        cloud_options,
                        "worker-pod-template",
                    ).to_dict(),
                )
            },
        )
