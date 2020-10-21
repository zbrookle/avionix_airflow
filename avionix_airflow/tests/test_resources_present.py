import pytest
from pytest_cases import fixture_ref, parametrize_plus

from avionix_airflow.kubernetes.services import AirflowService
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator
from avionix_airflow.tests.conftest import database_service, webserver_service
from avionix_airflow.tests.utils import (
    filter_out_pvc,
    kubectl_name_dict,
    skip_if_not_celery,
)


@parametrize_plus(
    "service", [fixture_ref(database_service), fixture_ref(webserver_service)]
)
def test_services_present(airflow_options, service: AirflowService):
    service_name = service.metadata.name
    if service_name in {"flower-svc", "redis-svc"}:
        skip_if_not_celery(airflow_options)

    service_info = kubectl_name_dict("service")
    assert service_info[service_name]["TYPE"] == "NodePort"

    def get_port(service: str):
        return service_info[service]["PORT(S)"][:4]

    assert get_port(service_name) == str(service.spec.ports[0].port)


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


def test_namespaces_present(airflow_options):
    assert airflow_options.namespace in kubectl_name_dict("namespace")
    if airflow_options.in_kube_mode:
        assert airflow_options.pods_namespace in kubectl_name_dict("namespace")
