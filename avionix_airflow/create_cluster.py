from avionix import ChartBuilder, ChartInfo
from avionix.errors import ChartAlreadyInstalledError
from avionix_airflow.docker._build_image import build_airflow_image

from avionix_airflow.kubernetes.airflow import AirflowOptions, AirflowOrchestrator
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator
from avionix_airflow.kubernetes.postgres import PostgresOrchestrator, SqlOptions
from avionix_airflow.kubernetes.redis import RedisOptions, RedisOrchestrator


def get_chart_builder(
    airflow_options: AirflowOptions,
    sql_options: SqlOptions = SqlOptions(),
    redis_options: RedisOptions = RedisOptions(),
):
    """
    :param sql_options:
    :param redis_options:
    :param airflow_options:
    :return: Avionix ChartBuilder object that can be used to install airflow
    """
    builder = ChartBuilder(
        ChartInfo(
            api_version="3.2.4", name="airflow", version="0.1.0", app_version="v1"
        ),
        (
            PostgresOrchestrator(sql_options)
            + AirflowOrchestrator(
                sql_options, redis_options, ValueOrchestrator(), airflow_options
            )
            + RedisOrchestrator(redis_options)
        ).get_kube_parts(),
        keep_chart=True,
    )
    return builder


from avionix_airflow.tests.utils import parse_shell_script, dag_copy_loc


def main():
    build_airflow_image()
    airflow_options = AirflowOptions(
        dag_sync_image="alpine/git",
        dag_sync_command=["/bin/sh", "-c", parse_shell_script(dag_copy_loc),],
        dag_sync_schedule="* * * * *",
    )
    get_chart_builder(airflow_options).install_chart()


if __name__ == "__main__":
    main()
