from avionix.kubernetes_objects.container import Container, ContainerPort
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix.kubernetes_objects.env import EnvVar
from typing import List, Optional


class AirflowContainer(Container):
    def __init__(
        self,
        name: str,
        args,
        sql_options: SqlOptions,
        ports: Optional[List[ContainerPort]] = None,
    ):
        super().__init__(
            name=name,
            args=args,
            image="airflow-image",
            image_pull_policy="Never",
            env=sql_options.get_airflow_environment()
            + [
                EnvVar(
                    "AIRFLOW__CORE__SQL_ALCHEMY_CONN",
                    sql_options.get_postgres_connection_string(),
                )
            ],
            ports=ports
        )


class WebserverUI(AirflowContainer):
    def __init__(self, sql_options: SqlOptions):
        super().__init__("webserver", ["webserver"], sql_options, ports=[
            ContainerPort(8080, None, host_port=8080)])


class Scheduler(AirflowContainer):
    def __init__(self, sql_options: SqlOptions):
        super().__init__("scheduler", ["scheduler"], sql_options)
