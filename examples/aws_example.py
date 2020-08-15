from avionix_airflow import (
    get_chart_builder,
    AirflowOptions,
    AwsOptions,
    SqlOptions,
    MonitoringOptions,
)

builder = get_chart_builder(
    airflow_options=AirflowOptions(
        dag_sync_image="alpine/git",
        dag_sync_command=["/bin/sh", "-c", "my_shell_commands",],
        dag_sync_schedule="* * * * *",
        default_timezone="est",
        core_executor="KubernetesExecutor",
        domain_name=None,
    ),
    monitoring_options=MonitoringOptions(
        elastic_search_uri="https://my-es-vpc.es.amazonaws.com",
    ),
    sql_options=SqlOptions(
        user="postgres-user",
        password="****",
        host="my-postgres-host.amazonaws.com",
        create_database_in_cluster=False,
    ),
    cloud_options=AwsOptions("fs-12345", "my-cluster", ""),
)
