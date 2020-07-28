import time

from avionix_airflow.tests.utils import kubectl_name_dict


def test_services_present(label):
    service_info = kubectl_name_dict("service")
    for service in service_info:
        assert service_info[service]["TYPE"] == "NodePort"

    def get_port(service_name: str):
        return service_info[service_name]["PORT(S)"][:4]

    assert get_port(label.database_service_name) == "5432"
    assert get_port(label.flower_service_name) == "5555"
    assert get_port(label.redis_service_name) == "6379"
    assert get_port(label.webserver_service_name) == "8080"


def test_deployments_present(label):
    deployment_info = kubectl_name_dict("deployment")
    time.sleep(5)
    for deployment in [
        label.master_deployment_name,
        label.redis_deployment_name,
        label.database_deployment_name,
    ]:
        assert deployment in deployment_info
        assert deployment_info[deployment]["READY"] == "1/1"


def test_volumes_present(label):
    volume_info = kubectl_name_dict("persistentvolume")
    for volume in volume_info:
        volume_specific_info = volume_info[volume]
        assert volume_specific_info["CAPACITY"] == "50Mi"
        assert volume_specific_info["ACCESS MODES"] == "RWX"
