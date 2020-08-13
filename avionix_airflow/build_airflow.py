from avionix import ChartBuilder, ChartInfo
from avionix.chart import ChartMaintainer

from avionix_airflow.kubernetes.airflow import AirflowOptions, AirflowOrchestrator
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.cloud.local.local_options import LocalOptions
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
    cloud_options: CloudOptions = LocalOptions(),
):
    """
    :param sql_options:
    :param redis_options:
    :param airflow_options:
    :param monitoring_options:
    :param cloud_options:
    :return: Avionix ChartBuilder object that can be used to install airflow
    """
    orchestrator = AirflowOrchestrator(
        sql_options,
        redis_options,
        ValueOrchestrator(),
        airflow_options,
        monitoring_options,
        cloud_options,
    )
    dependencies = cloud_options.get_cloud_dependencies()
    if monitoring_options.enabled:
        dependencies += [
            GrafanaDependency(
                monitoring_options, airflow_options, sql_options, cloud_options
            ),
            TelegrafDependency(monitoring_options, cloud_options),
            FileBeatDependency(monitoring_options, cloud_options),
        ]
        if monitoring_options.enable_elasticsearch_dependency:
            dependencies.append(ElasticSearchDependency())
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
    builder.kubernetes_objects += cloud_options.get_platform_dependent_kube_objects()
    return builder
