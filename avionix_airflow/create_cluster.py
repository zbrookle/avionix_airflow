from avionix import ChartBuilder, ChartInfo

from avionix_airflow.docker._build_image import build_airflow_image
from avionix_airflow.host_settings import add_host
from avionix_airflow.kubernetes.airflow import AirflowOptions, AirflowOrchestrator
from avionix_airflow.kubernetes.postgres import PostgresOrchestrator, SqlOptions
from avionix_airflow.kubernetes.redis import RedisOptions, RedisOrchestrator
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


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
    orchestrator = PostgresOrchestrator(sql_options) + AirflowOrchestrator(
        sql_options, redis_options, ValueOrchestrator(), airflow_options
    )
    if airflow_options.in_celery_mode:
        orchestrator += RedisOrchestrator(redis_options)
    builder = ChartBuilder(
        ChartInfo(
            api_version="3.2.4", name="airflow", version="0.1.0", app_version="v1"
        ),
        orchestrator.get_kube_parts(),
        keep_chart=True,
    )
    return builder


from avionix_airflow.tests.utils import TEST_AIRFLOW_OPTIONS


def main():
    build_airflow_image()
    add_host(TEST_AIRFLOW_OPTIONS)
    get_chart_builder(TEST_AIRFLOW_OPTIONS).install_chart()


if __name__ == "__main__":
    main()
