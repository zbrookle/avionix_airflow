from avionix_airflow.kubernetes.label_handler import LabelHandler
import pytest


@pytest.fixture
def label():
    return LabelHandler()
