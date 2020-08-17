from typing import List

from avionix import ChartBuilder, ChartDependency, ChartInfo
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


class AvionixChartInfo(ChartInfo):
    def __init__(self, name: str, dependencies: List[ChartDependency]):
        super().__init__(
            api_version="3.2.4",
            name=name,
            version="0.1.0",
            app_version="v1",
            maintainers=[ChartMaintainer("Zach Brookler", "zachb1996@yahoo.com")],
            dependencies=dependencies,
        )


def get_chart_builder(
    airflow_options: AirflowOptions,
    sql_options: SqlOptions = SqlOptions(),
    redis_options: RedisOptions = RedisOptions(),
    monitoring_options: MonitoringOptions = MonitoringOptions(),
    cloud_options: CloudOptions = LocalOptions(),
) -> ChartBuilder:
    """
    :param sql_options: An SqlOptions object
    :param redis_options: A RedisOptions object
    :param airflow_options: An AirflowOptions object
    :param monitoring_options: A MonitoringOptions object
    :param cloud_options: A CloudOptions object
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
        AvionixChartInfo("airflow", dependencies),
        orchestrator.get_kube_parts(),
        namespace=airflow_options.namespace,
    )
    builder.kubernetes_objects += cloud_options.get_platform_dependent_kube_objects()
    if (
        monitoring_options.enabled
        and not monitoring_options.enable_elasticsearch_dependency
    ):
        builder.kubernetes_objects += cloud_options.get_elastic_search_proxy_elements(
            monitoring_options.elastic_search_uri
        )
    return builder
