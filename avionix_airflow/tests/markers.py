import pytest

from avionix_airflow.tests.utils import TEST_AIRFLOW_OPTIONS

network_test = pytest.mark.flaky(reruns=5, reruns_delay=2)
celery_only_test = pytest.mark.skipif(
    TEST_AIRFLOW_OPTIONS.core_executor != "CeleryExecutor",
    reason="This functionality is only available " "with the celery executor",
)
