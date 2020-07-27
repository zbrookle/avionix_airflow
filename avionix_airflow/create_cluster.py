from avionix import ChartBuilder, ChartInfo
from avionix.errors import ChartAlreadyInstalledError
from docker.build_image import build_airflow_image

from avionix_airflow.kubernetes.airflow import AirflowOptions, AirflowOrchestrator
from avionix_airflow.kubernetes.label_handler import LabelHandler
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
                sql_options, redis_options, LabelHandler(), airflow_options
            )
            + RedisOrchestrator(redis_options)
        ).get_kube_parts(),
        keep_chart=True,
    )
    return builder


def main():
    airflow_options = AirflowOptions(
        dag_sync_image="busybox",
        dag_sync_command=[
            "git",
            "clone",
            "https://github.com/zbrookle/avionix_airflow_test_dags",
            "/tmp/dags;",
            "cp",
            "/tmp/dags/*",
            "/home/airflow/dags",
        ],
        dag_sync_schedule="* * * * *",
    )
    get_chart_builder(airflow_options).install_chart()


if __name__ == "__main__":
    main()
