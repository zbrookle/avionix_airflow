import pytest

from avionix_airflow.kubernetes.airflow import AirflowOptions

network_test = pytest.mark.flaky(reruns=5, reruns_delay=2)
