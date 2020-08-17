from avionix.kube.apps import Deployment, DeploymentSpec
from avionix.kube.core import Container, ContainerPort, PodSpec, PodTemplateSpec
from avionix.kube.meta import LabelSelector

from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class PostgresPodTemplate(PodTemplateSpec):
    def __init__(self, sql_options: SqlOptions):
        super().__init__(
            AirflowMeta(
                name="postgres-database-pod", labels=ValueOrchestrator().database_labels
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
                LabelSelector(ValueOrchestrator().database_labels),
            ),
        )
