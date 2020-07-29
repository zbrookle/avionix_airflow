from telnetlib import Telnet

import pytest

from avionix_airflow.kubernetes.airflow.airflow_service import (
    FlowerService,
    WebserverService,
)
from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.kubernetes.postgres.database_service import DatabaseService
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator
from avionix_airflow.tests.utils import TEST_AIRFLOW_OPTIONS


def get_node_port(service: AirflowService):
    return service.spec.ports[0].nodePort


@pytest.mark.skipif(TEST_AIRFLOW_OPTIONS.core_executor != "CeleryExecutor",
                    reason="Only celery executor uses flower")
def test_flower_connections(host):
    Telnet(host=host, port=get_node_port(FlowerService(ValueOrchestrator())))


@pytest.mark.parametrize(
    "service", [WebserverService(ValueOrchestrator()), DatabaseService(SqlOptions()),],
)
def test_connections(service, host):
    Telnet(host=host, port=get_node_port(service))
