import time

from avionix.errors import NamespaceBeingTerminatedError
from avionix.testing.installation_context import ChartInstallationContext
import pytest

from avionix_airflow import get_chart_builder
from avionix_airflow.kubernetes.label_handler import LabelHandler
from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.tests.utils import parse_shell_script, dag_copy_loc

@pytest.fixture
def label():
    return LabelHandler()


@pytest.fixture
def airflow_options():
    return AirflowOptions(
        dag_sync_image="alpine/git",
        dag_sync_command=["/bin/sh", "-c", parse_shell_script(dag_copy_loc),],
        dag_sync_schedule="* * * * *",
    )


@pytest.fixture(scope="session", autouse=True)
def build_chart(airflow_options):
    builder = get_chart_builder(airflow_options)
    try:
        with ChartInstallationContext(builder):
            yield
    except NamespaceBeingTerminatedError:
        builder.uninstall_chart()
        time.sleep(7)
        with ChartInstallationContext(builder):
            yield
