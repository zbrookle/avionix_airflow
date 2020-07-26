from subprocess import check_output
from telnetlib import Telnet

import pytest

from avionix_airflow.kubernetes.airflow.airflow_service import (
    FlowerService,
    WebserverService,
)
from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.kubernetes.label_handler import LabelHandler
from avionix_airflow.kubernetes.postgres.database_service import DatabaseService
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions


@pytest.fixture
def host():
    return check_output(["minikube", "ip"]).decode("utf-8").strip()


def get_node_port(service: AirflowService):
    return service.spec.ports[0].nodePort


services = [
    WebserverService(LabelHandler()),
    FlowerService(LabelHandler()),
    DatabaseService(SqlOptions()),
]


@pytest.mark.parametrize(
    "service",
    [
        WebserverService(LabelHandler()),
        FlowerService(LabelHandler()),
        DatabaseService(SqlOptions()),
    ],
)
def test_connections(service, host):
    Telnet(host=host, port=get_node_port(service))
