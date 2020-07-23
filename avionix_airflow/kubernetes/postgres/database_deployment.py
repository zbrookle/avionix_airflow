from avionix.kubernetes_objects.pod import (
    Container,
    PodSpec,
    PodTemplateSpec,
    LabelSelector,
)
from avionix.kubernetes_objects.deployment import Deployment, DeploymentSpec
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.label_handler import LabelHandler


class PostgresPodTemplate(PodTemplateSpec):
    def __init__(self, sql_options: SqlOptions):
        super().__init__(
            AirflowMeta(
                name="postgres-database-pod", labels=LabelHandler().database_labels
            ),
            spec=PodSpec(
                [
                    Container(
                        name="postgres-database",
                        image="postgres",
                        env=sql_options.get_postgres_envioronment(),
                    )
                ]
            ),
        )


class DatabaseDeployment(Deployment):
    def __init__(self, sql_options: SqlOptions):
        super().__init__(
            AirflowMeta(name="postgres-database-deployment"),
            DeploymentSpec(
                PostgresPodTemplate(sql_options),
                LabelSelector(LabelHandler().database_labels),
            ),
        )
