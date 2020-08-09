import pytest

from avionix_airflow.kubernetes.value_handler import ValueOrchestrator
from avionix_airflow.tests.utils import (
    filter_out_pvc,
    kubectl_name_dict,
    skip_if_not_celery,
)


@pytest.fixture(
    params=[
        ValueOrchestrator().database_service_name,
        ValueOrchestrator().webserver_service_name,
        ValueOrchestrator().flower_service_name,
        ValueOrchestrator().redis_service_name,
    ]
)
def service_name(request):
    return request.param


@pytest.fixture
def port_mapping(label):
    return {
        label.redis_service_name: "6379",
        label.flower_service_name: "5555",
        label.webserver_service_name: "8080",
        label.database_service_name: "5432",
    }


def test_services_present(label, airflow_options, service_name, port_mapping):
    if service_name in {label.flower_service_name, label.redis_service_name}:
        skip_if_not_celery(airflow_options)

    service_info = kubectl_name_dict("service")
    assert service_info[service_name]["TYPE"] == "NodePort"

    def get_port(service: str):
        return service_info[service]["PORT(S)"][:4]

    assert get_port(service_name) == port_mapping[service_name]


@pytest.fixture(
    params=[
        ValueOrchestrator().master_deployment_name,
        ValueOrchestrator().redis_deployment_name,
        ValueOrchestrator().database_deployment_name,
    ]
)
def deployment(request):
    return request.param


def test_deployments_present(deployment, label, airflow_options):
    if deployment == label.redis_deployment_name:
        skip_if_not_celery(airflow_options)
    deployment_info = kubectl_name_dict("deployment")
    assert deployment in deployment_info
    assert deployment_info[deployment]["READY"] == "1/1"


def test_volumes_present(label):
    volume_info = filter_out_pvc(kubectl_name_dict("persistentvolume"))
    for volume in volume_info:
        volume_specific_info = volume_info[volume]
        assert volume_specific_info["CAPACITY"] == "50Mi"
        assert volume_specific_info["ACCESS MODES"] == "RWX"
