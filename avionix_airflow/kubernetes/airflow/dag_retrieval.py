from avionix.kubernetes_objects.batch import (
    CronJob,
    CronJobSpec,
    JobTemplateSpec,
    JobSpec,
)
from avionix.kubernetes_objects.core import PodTemplateSpec, PodSpec, Container
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.airflow.airflow_storage import AirflowDagVolumeGroup
from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions


class DagRetrievalJob(CronJob):
    def __init__(
        self, airflow_options: AirflowOptions,
    ):
        dag_volume_group = AirflowDagVolumeGroup(airflow_options)
        super().__init__(
            AirflowMeta("dag-sync-job"),
            spec=CronJobSpec(
                JobTemplateSpec(
                    JobSpec(
                        PodTemplateSpec(
                            AirflowMeta("sync-dags-pod",),
                            PodSpec(
                                [
                                    Container(
                                        "sync-dag-container",
                                        image=airflow_options.dag_sync_image,
                                        command=airflow_options.dag_sync_command,
                                        image_pull_policy="IfNotPresent",
                                        volume_mounts=[dag_volume_group.volume_mount],
                                    )
                                ],
                                volumes=[dag_volume_group.volume],
                                restart_policy="OnFailure",
                            ),
                        ),
                    )
                ),
                airflow_options.dag_sync_schedule,
            ),
        )
