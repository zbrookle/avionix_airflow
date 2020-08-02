from avionix import ChartBuilder, ChartInfo
from avionix.chart import ChartMaintainer, ChartDependency

from avionix_airflow.kubernetes.airflow import AirflowOptions, AirflowOrchestrator
from avionix_airflow.kubernetes.postgres import PostgresOrchestrator, SqlOptions
from avionix_airflow.kubernetes.redis import RedisOptions, RedisOrchestrator
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


def get_chart_builder(
    airflow_options: AirflowOptions,
    sql_options: SqlOptions = SqlOptions(),
    redis_options: RedisOptions = RedisOptions(),
    monitoring: bool = True,
):
    """
    :param sql_options:
    :param redis_options:
    :param airflow_options:
    :return: Avionix ChartBuilder object that can be used to install airflow
    """
    orchestrator = AirflowOrchestrator(
        sql_options, redis_options, ValueOrchestrator(), airflow_options
    )
    dependencies = []
    if monitoring:
        dependencies = [
            ChartDependency(
                "elasticsearch",
                "7.8.1",
                "https://helm.elastic.co",
                "elastic",
                values={
                    "replicas": 1,
                    "minimumMasterNodes": 1,
                    "antiAffinity": "soft",
                    "esJavaOpts": "-Xmx128m -Xms128m",
                    "resources": {
                        "requests": {"cpu": "100m", "memory": "512M"},
                        "limits": {"cpu": "1000m", "memory": "512M"},
                    },
                    "volumeClaimTemplate": {
                        "accessModes": ["ReadWriteOnce"],
                        "storageClassName": "standard",
                        "resources": {"requests": {"storage": "100M"}},
                    },
                },
            ),
            ChartDependency(
                "telegraf",
                "1.7.21",
                "https://helm.influxdata.com/",
                "influxdata",
                values={
                    "replicaCount": 1,
                    "env": [{"name": "HOSTNAME", "value": "telegraf"}],
                    "service": {
                        "enabled": True,
                        "type": "ClusterIP",
                        "annotations": {},
                    },
                    "serviceAccount": {"create": True},
                    "config": {
                        "outputs": [
                            {
                                "elasticsearch": {
                                    "urls": ["http://elasticsearch-master:9200"],
                                    "timeout": "5s",
                                    "health_check_interval": "10s",
                                    "index_name": "airflow-%Y.%m.%d",
                                    "manage_template": True,
                                    "template_name": "airflow",
                                    "overwrite_template": False,
                                }
                            }
                        ],
                        "inputs": [{"statsd": {"service_address": ":8125"}}],
                    },
                },
            ),
            ChartDependency(
                "grafana",
                "5.5.2",
                "https://kubernetes-charts.storage.googleapis.com/",
                "stable",
                values={
                    "grafana.ini": {
                        "server": {
                            "domain": "www.avionix-airflow.com",
                            "root_url": "%(protocol)s://%(domain)s/grafana",
                            "serve_from_sub_path": True,
                        },
                        "auth.anonymous": {
                            "enabled": True,
                            "org_name": "Main Org.",
                            "org_role": "Admin",
                        },
                        "auth.basic": {"enabled": False},
                    }
                },
            ),
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
        create_namespace=True,
    )
    return builder
