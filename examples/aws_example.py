from avionix_airflow import (
    AirflowOptions,
    AwsOptions,
    MonitoringOptions,
    SqlOptions,
    get_chart_builder,
)

builder = get_chart_builder(
    airflow_options=AirflowOptions(
        dag_sync_image="alpine/git",
        dag_sync_command=["/bin/sh", "-c", "my_shell_commands"],
        dag_sync_schedule="* * * * *",
        default_timezone="est",
        core_executor="KubernetesExecutor",
        domain_name="my.airflow.domain.com",
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
    cloud_options=AwsOptions(
        efs_id="fs-12345",
        cluster_name="my-cluster",
        elastic_search_access_role_arn="arn:aws:iam::123456789012:role/es-role",
        default_role_arn="arn:aws:iam::123456789012:role/default-role",
        alb_role_arn="arn:aws:iam::123456789012:role/alb-role",
        external_dns_role_arn="arn:aws:iam::123456789012:role/external-dns-role",
        autoscaling_role_arn="arn:aws:iam::123456789012:role/autoscaling-role",
        domain="my.airflow.domain.com",
        dag_sync_role_arn="arn:aws:iam::123456789012:role/dag_sync_role",
        use_ssl=True,
    ),
)
