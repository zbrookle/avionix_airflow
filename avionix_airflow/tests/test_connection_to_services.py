from telnetlib import Telnet

from pytest_cases import fixture_ref, parametrize_plus

from avionix_airflow.kubernetes.airflow.airflow_service import FlowerService
from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.kubernetes.cloud.local.local_options import LocalOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator
from avionix_airflow.tests.conftest import database_service, webserver_service
from avionix_airflow.tests.utils import skip_if_not_celery


def get_node_port(service: AirflowService):
    return service.spec.ports[0].nodePort


@parametrize_plus(
    "service",
    [
        fixture_ref(webserver_service),
        fixture_ref(database_service),
        FlowerService(
            ValueOrchestrator(), node_ports_open=True, cloud_options=LocalOptions()
        ),
    ],
)
def test_connections(service, host, airflow_options):
    if isinstance(service, FlowerService):
        skip_if_not_celery(airflow_options)
    Telnet(host=host, port=get_node_port(service))
