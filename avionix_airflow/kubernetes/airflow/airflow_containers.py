from avionix.kubernetes_objects.pod import Container
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix.kubernetes_objects.env import EnvVar


class AirflowContainer(Container):
    def __init__(self, name, args, sql_options: SqlOptions):
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
        )


class WebserverUI(AirflowContainer):
    def __init__(self, sql_options: SqlOptions):
        super().__init__("webserver", ["webserver"], sql_options)


class Scheduler(AirflowContainer):
    def __init__(self, sql_options: SqlOptions):
        super().__init__("scheduler", ["scheduler"], sql_options)
