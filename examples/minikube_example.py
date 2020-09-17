import logging

from avionix_airflow import add_host, build_airflow_image, get_chart_builder
from avionix_airflow.kubernetes.airflow import AirflowOptions
from avionix_airflow.kubernetes.monitoring import MonitoringOptions
from avionix_airflow.tests.utils import dag_copy_loc, parse_shell_script

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
logging.basicConfig(format="[%(filename)s:%(lineno)s] %(message)s", level=logging.INFO)


def install_chart():
    build_airflow_image()
    airflow_options = AirflowOptions(
        dag_sync_image="alpine/git",
        dag_sync_command=["/bin/sh", "-c", parse_shell_script(str(dag_copy_loc))],
        dag_sync_schedule="* * * * *",
        default_timezone="est",
        core_executor="KubernetesExecutor",
        open_node_ports=True,
        image_pull_policy="Never",
    )
    add_host(airflow_options)
    builder = get_chart_builder(
        airflow_options=airflow_options,
        monitoring_options=MonitoringOptions(grafana_role="Admin"),
    )
    if builder.is_installed:
        builder.upgrade_chart({"dependency-update": None})
        return
    builder.install_chart(options={"create-namespace": None, "dependency-update": None})
