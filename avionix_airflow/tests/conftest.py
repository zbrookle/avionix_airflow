import os
import time

from avionix.errors import NamespaceBeingTerminatedError
from avionix.testing import ChartInstallationContext
import pytest

from avionix_airflow import get_chart_builder
from avionix_airflow.kubernetes.label_handler import LabelHandler


@pytest.fixture
def label():
    return LabelHandler()


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
