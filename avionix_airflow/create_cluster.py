from avionix import ChartBuilder, ChartInfo
from docker.build_image import build_airflow_image
from avionix_airflow.kubernetes.airflow import AirflowOrchestrator
from avionix_airflow.kubernetes.postgres import PostgresOrchestrator, SqlOptions
from avionix_airflow.kubernetes.redis import RedisOrchestrator, RedisOptions
from avionix.errors import ChartAlreadyInstalledError


def get_chart_builder():
    sql_options = SqlOptions()
    redis_options = RedisOptions()
    builder = ChartBuilder(
        ChartInfo(
            api_version="3.2.4", name="airflow", version="0.1.0", app_version="v1"
        ),
        (
            PostgresOrchestrator(sql_options)
            + AirflowOrchestrator(sql_options, redis_options)
            + RedisOrchestrator(redis_options)
        ).get_kube_parts(),
    )
    return builder


def install_chart():
    build_airflow_image()
    get_chart_builder().install_chart()


def uninstall_chart():
    get_chart_builder().uninstall_chart()


def create_airflow_cluster():
    install_chart()


def main():
    try:
        create_airflow_cluster()
    except ChartAlreadyInstalledError:
        uninstall_chart()
        create_airflow_cluster()


if __name__ == "__main__":
    main()
