from logging import info
from subprocess import check_output

from avionix.testing.installation_context import ChartInstallationContext
from pandas import DataFrame
import pytest
from pytest_cases import fixture_plus, fixture_ref, parametrize_plus

from avionix_airflow import get_chart_builder
from avionix_airflow.docker import build_airflow_image
from avionix_airflow.host_settings import add_host
from avionix_airflow.kubernetes.airflow import AirflowOptions
from avionix_airflow.kubernetes.cloud.local.local_options import LocalOptions
from avionix_airflow.kubernetes.monitoring import MonitoringOptions
from avionix_airflow.kubernetes.postgres import SqlOptions
from avionix_airflow.kubernetes.redis import RedisOptions
from avionix_airflow.kubernetes.services import ServiceFactory
from avionix_airflow.kubernetes.utils import get_minikube_ip
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator
from avionix_airflow.teardown_cluster import teardown
from avionix_airflow.tests.utils import (
    dag_copy_loc,
    filter_out_pvc,
    kubectl_name_dict,
    parse_shell_script,
)


class AvionixAirflowChartInstallationContext(ChartInstallationContext):
    def get_status_resources(self):
        resources = DataFrame(super().get_status_resources())
        new_resources = resources.filter(regex=".*deployment.*")
        return new_resources


@pytest.fixture
def label():
    return ValueOrchestrator()


@pytest.fixture
def host():
    return get_minikube_ip()


@fixture_plus(scope="session")
@parametrize_plus("namespace", ["", "airflow-worker-pods"])
def pod_namespace(namespace):
    return namespace


@fixture_plus(scope="session")
@parametrize_plus("executor_name", ["CeleryExecutor", "KubernetesExecutor"])
def executor(executor_name):
    return executor_name


@parametrize_plus(
    "executor, pod_namespace", [(fixture_ref(executor), fixture_ref(pod_namespace))]
)
@pytest.fixture(scope="session")
def airflow_options(executor, pod_namespace):
    return AirflowOptions(
        dag_sync_image="alpine/git",
        dag_sync_command=["/bin/sh", "-c", parse_shell_script(str(dag_copy_loc))],
        dag_sync_schedule="* * * * *",
        default_timezone="est",
        core_executor=executor,
        open_node_ports=True,
        local_mode=True,
        pods_namespace=pod_namespace,
    )


@pytest.fixture(scope="session")
def monitoring_options():
    return MonitoringOptions(grafana_role="Admin")


@pytest.fixture(scope="session")
def redis_options():
    return RedisOptions()


@pytest.fixture(scope="session")
def sql_options():
    return SqlOptions()


@pytest.fixture(scope="session")
def cloud_options():
    return LocalOptions()


@pytest.fixture
def service_factory(sql_options, cloud_options, airflow_options):
    return ServiceFactory(sql_options, cloud_options, airflow_options)


@fixture_plus
def webserver_service(service_factory):
    return service_factory.webserver_service


@fixture_plus
def database_service(service_factory):
    return service_factory.database_service


@fixture_plus
def flower_service(service_factory):
    return service_factory.flower_service


def deployments_are_ready():
    deployments = kubectl_name_dict("deployment")
    for deployment in deployments:
        if deployments[deployment]["READY"] != "1/1":
            return False
    return True


@pytest.fixture(scope="session", autouse=True)
def build_chart(
    airflow_options, sql_options, redis_options, monitoring_options, cloud_options
):
    add_host(airflow_options, force=True)
    build_airflow_image()
    builder = get_chart_builder(
        airflow_options, sql_options, redis_options, monitoring_options, cloud_options
    )
    if kubectl_name_dict("persistentvolume"):
        # Stateful Sets do not automatically clean up their pvc templates so this
        # must be done manually
        info(check_output("kubectl delete pvc -n airflow --all".split(" ")))
    while True:
        if not filter_out_pvc(kubectl_name_dict("persistentvolume")):
            break
    with AvionixAirflowChartInstallationContext(
        builder,
        expected_status={"1/1", "3/3"},
        status_field="READY",
        uninstall_func=lambda: teardown(builder),
    ):
        while True:
            if deployments_are_ready():
                break
        yield
