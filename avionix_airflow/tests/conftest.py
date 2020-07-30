import time

from avionix.errors import NamespaceBeingTerminatedError
from avionix.testing.installation_context import ChartInstallationContext
import pytest

from avionix_airflow import get_chart_builder
from avionix_airflow.docker import build_airflow_image
from avionix_airflow.host_settings import add_host
from avionix_airflow.kubernetes.postgres import SqlOptions
from avionix_airflow.kubernetes.redis import RedisOptions
from avionix_airflow.kubernetes.utils import get_minikube_ip
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator
from avionix_airflow.teardown_cluster import teardown
from avionix_airflow.tests.utils import TEST_AIRFLOW_OPTIONS, kubectl_name_dict


@pytest.fixture
def label():
    return ValueOrchestrator()


@pytest.fixture
def host():
    return get_minikube_ip()


@pytest.fixture(scope="session", params=["CeleryExecutor", "KubernetesExecutor"])
def airflow_options(request):
    options = TEST_AIRFLOW_OPTIONS
    TEST_AIRFLOW_OPTIONS.core_executor = request.param
    return options


@pytest.fixture(scope="session")
def redis_options():
    return RedisOptions()


@pytest.fixture(scope="session")
def sql_options():
    return SqlOptions()


def deployments_are_ready(deployments: dict):
    for deployment in deployments:
        if deployments[deployment]["READY"] != "1/1":
            return False
    return True


@pytest.fixture(scope="session", autouse=True)
def build_chart(airflow_options, sql_options, redis_options):
    add_host(airflow_options, force=True)

    build_airflow_image()
    builder = get_chart_builder(airflow_options, sql_options, redis_options)
    try:
        with ChartInstallationContext(
            builder, expected_status={"1/1", "3/3"}, status_field="READY",
                uninstall_func=lambda: teardown(builder)
        ):
            while True:
                deployments = kubectl_name_dict("deployments")
                if deployments_are_ready(deployments):
                    break
            yield
    except NamespaceBeingTerminatedError:
        builder.uninstall_chart()
        time.sleep(7)
        with ChartInstallationContext(builder):
            yield
    else:
        if builder.is_installed:
            teardown(builder)
