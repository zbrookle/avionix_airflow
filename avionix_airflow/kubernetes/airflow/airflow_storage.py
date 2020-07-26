from avionix.kubernetes_objects.core import (
    Volume,
    PersistentVolumeClaim,
    PersistentVolume,
    PersistentVolumeSpec,
    HostPathVolumeSource,
)
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions


class AirflowVolume(PersistentVolume):
    def __init__(self, name: str, storage: str, host_path: str):
        super().__init__(
            AirflowMeta(name),
            PersistentVolumeSpec(
                ["ReadWriteMany"],
                capacity={"storage": storage},
                host_path=HostPathVolumeSource(host_path, type="DirectoryOrCreate"),
            ),
        )


class AirflowLogVolume(AirflowVolume):
    def __init__(self, options: AirflowOptions):
        super().__init__(
            "log-volume", options.log_storage, host_path="/home/airflow/logs"
        )


class AirflowDagVolume(AirflowVolume):
    def __init__(self, options: AirflowOptions):
        super().__init__(
            "dags-volume", options.dag_storage, host_path="/home/airflow/dags"
        )
