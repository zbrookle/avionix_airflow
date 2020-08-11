from avionix import ChartBuilder, ChartInfo
from avionix.chart import ChartMaintainer

from avionix_airflow.kubernetes.airflow import AirflowOptions, AirflowOrchestrator
from avionix_airflow.kubernetes.monitoring import (
    ElasticSearchDependency,
    FileBeatDependency,
    GrafanaDependency,
    MonitoringOptions,
    TelegrafDependency,
)
from avionix_airflow.kubernetes.postgres import PostgresOrchestrator, SqlOptions
from avionix_airflow.kubernetes.redis import RedisOptions, RedisOrchestrator
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


def get_chart_builder(
    airflow_options: AirflowOptions,
    sql_options: SqlOptions = SqlOptions(),
    redis_options: RedisOptions = RedisOptions(),
    monitoring_options: MonitoringOptions = MonitoringOptions(),
):
    """
    :param sql_options:
    :param redis_options:
    :param airflow_options:
    :param monitoring_options:
    :return: Avionix ChartBuilder object that can be used to install airflow
    """
    orchestrator = AirflowOrchestrator(
        sql_options,
        redis_options,
        ValueOrchestrator(),
        airflow_options,
        monitoring_options,
    )
    dependencies = []
    if monitoring_options.enabled:
        dependencies = [
            ElasticSearchDependency(),
            GrafanaDependency(monitoring_options, airflow_options, sql_options),
            TelegrafDependency(),
            FileBeatDependency(monitoring_options),
        ]
    if airflow_options.in_celery_mode:
        orchestrator += RedisOrchestrator(redis_options)
    if sql_options.create_database_in_cluster:
        orchestrator += PostgresOrchestrator(sql_options)
    builder = ChartBuilder(
        ChartInfo(
            api_version="3.2.4",
            name="airflow",
            version="0.1.0",
            app_version="v1",
            maintainers=[ChartMaintainer("Zach Brookler", "zachb1996@yahoo.com")],
            dependencies=dependencies,
        ),
        orchestrator.get_kube_parts(),
        namespace=airflow_options.namespace,
    )
    return builder
