from telnetlib import Telnet

from pytest_cases import fixture_ref, parametrize_plus

from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.tests.conftest import (
    database_service,
    flower_service,
    webserver_service,
)
from avionix_airflow.tests.utils import skip_if_not_celery


def get_node_port(service: AirflowService):
    return service.spec.ports[0].nodePort


@parametrize_plus(
    "service",
    [
        fixture_ref(webserver_service),
        fixture_ref(database_service),
        fixture_ref(flower_service),
    ],
)
def test_connections(service: AirflowService, host, airflow_options):
    if service.metadata.name == "flower-svc":
        skip_if_not_celery(airflow_options)
    Telnet(host=host, port=get_node_port(service))
