from avionix.kube.batch import CronJob, CronJobSpec, JobSpec, JobTemplateSpec
from avionix.kube.core import Container, PodSpec, PodTemplateSpec

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.airflow.airflow_storage import AirflowDagVolumeGroup
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta


class DagRetrievalJob(CronJob):
    def __init__(self, airflow_options: AirflowOptions, cloud_options: CloudOptions):
        dag_volume_group = AirflowDagVolumeGroup(airflow_options, cloud_options)
        super().__init__(
            AirflowMeta("dag-sync-job"),
            spec=CronJobSpec(
                JobTemplateSpec(
                    JobSpec(
                        PodTemplateSpec(
                            AirflowMeta(
                                "sync-dags-pod",
                                annotations=cloud_options.dag_retrieval_annotations,
                            ),
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
