from avionix_airflow import get_chart_builder
from avionix.testing import ChartInstallationContext, kubectl_get


def kubectl_get_airflow(resource: str):
    return kubectl_get(resource, "airflow")


def kubectl_name_dict(resource: str):
    info = kubectl_get_airflow(resource)
    info_dict = {}
    for name in info["NAME"]:
        filtered = info[info["NAME"] == name].reset_index()
        columns = [
            column for column in filtered.columns if column not in {"NAME", "index"}
        ]
        info_dict[name] = {column: filtered[column][0] for column in columns}
    return info_dict


def test_resources_present(label):
    with ChartInstallationContext(get_chart_builder()):
        # Check services
        service_info = kubectl_name_dict("service")
        for service in service_info:
            assert service_info[service]["TYPE"] == "NodePort"

        def get_port(service_name: str):
            return service_info[service_name]["PORT(S)"][:4]

        assert get_port(label.database_service_name) == "5432"
        assert get_port(label.flower_service_name) == "5555"
        assert get_port(label.redis_service_name) == "6379"
        assert get_port(label.webserver_service_name) == "8080"

        # Check deployments
        deployment_info = kubectl_name_dict("deployment")
        for deployment in [
            label.master_deployment_name,
            label.redis_deployment_name,
            label.database_deployment_name,
        ]:
            assert deployment in deployment_info
