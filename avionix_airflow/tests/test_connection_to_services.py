from subprocess import check_output
from telnetlib import Telnet

import pytest

from avionix_airflow.kubernetes.airflow.airflow_service import (
    FlowerService,
    WebserverService,
)
from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.kubernetes.postgres.database_service import DatabaseService
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.utils import get_minikube_ip
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator
from avionix_airflow.tests.markers import network_test


@pytest.fixture
def host():
    return get_minikube_ip()


def get_node_port(service: AirflowService):
    return service.spec.ports[0].nodePort


services = [
    WebserverService(ValueOrchestrator()),
    FlowerService(ValueOrchestrator()),
    DatabaseService(SqlOptions()),
]


@pytest.mark.parametrize(
    "service",
    [
        WebserverService(ValueOrchestrator()),
        FlowerService(ValueOrchestrator()),
        DatabaseService(SqlOptions()),
    ],
)
@network_test
def test_connections(service, host):
    Telnet(host=host, port=get_node_port(service))
