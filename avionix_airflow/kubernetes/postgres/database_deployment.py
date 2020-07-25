from avionix.kubernetes_objects.apps import Deployment, DeploymentSpec
from avionix.kubernetes_objects.core import (
    Container,
    ContainerPort,
    PodSpec,
    PodTemplateSpec,
)
from avionix.kubernetes_objects.meta import LabelSelector

from avionix_airflow.kubernetes.label_handler import LabelHandler
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions


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
                        ports=[ContainerPort(5432, name="postgres")],
                        image_pull_policy="IfNotPresent",
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
