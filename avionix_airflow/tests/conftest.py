import time

from avionix.errors import NamespaceBeingTerminatedError
from avionix.testing.installation_context import ChartInstallationContext
import pytest

from avionix_airflow import get_chart_builder
from avionix_airflow.kubernetes.label_handler import LabelHandler
from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions


@pytest.fixture
def label():
    return LabelHandler()


@pytest.fixture
def airflow_options():
    return AirflowOptions(
        dag_sync_image="busybox",
        dag_sync_command=[
            "git",
            "clone",
            "https://github.com/zbrookle/avionix_airflow_test_dags",
            "/tmp/dags;",
            "cp",
            "/tmp/dags/*",
            "/home/airflow/dags",
        ],
        dag_sync_schedule="* * * * *",
    )


@pytest.fixture(scope="session", autouse=True)
def build_chart():
    try:
        with ChartInstallationContext(get_chart_builder()):
            yield
    except NamespaceBeingTerminatedError:
        get_chart_builder().uninstall_chart()
        time.sleep(7)
        with ChartInstallationContext(get_chart_builder()):
            yield
