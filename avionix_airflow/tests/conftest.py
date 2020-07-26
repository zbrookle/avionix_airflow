from avionix_airflow.kubernetes.label_handler import LabelHandler
import pytest
from avionix_airflow import get_chart_builder
from avionix.testing import ChartInstallationContext

@pytest.fixture
def label():
    return LabelHandler()

@pytest.fixture(scope="session", autouse=True)
def build_chart():
    with ChartInstallationContext(get_chart_builder()):
        yield
