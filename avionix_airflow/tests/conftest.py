import time

from avionix.errors import NamespaceBeingTerminatedError
from avionix.testing.installation_context import ChartInstallationContext
import pytest

from avionix_airflow import get_chart_builder
from avionix_airflow.docker import build_airflow_image
from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator
from avionix_airflow.tests.utils import TEST_AIRFLOW_OPTIONS, kubectl_name_dict
from avionix_airflow.teardown_cluster import teardown


@pytest.fixture
def label():
    return ValueOrchestrator()


@pytest.fixture(scope="session")
def airflow_options():
    return TEST_AIRFLOW_OPTIONS


def deployments_are_ready(deployments: dict):
    for deployment in deployments:
        if deployments[deployment]["READY"] != "1/1":
            return False
    return True


@pytest.fixture(scope="session", autouse=True)
def build_chart(airflow_options):
    build_airflow_image()
    builder = get_chart_builder(airflow_options)
    try:
        with ChartInstallationContext(builder,):
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
