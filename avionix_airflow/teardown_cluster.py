from avionix import ChartBuilder
from avionix.testing import kubectl_get


def teardown(builder: ChartBuilder):
    builder.uninstall_chart()
    print("Terminating...")
    while True:
        namespaces_info = kubectl_get("namespace")
        names = namespaces_info["NAME"]
        if "airflow" not in names.values:
            break
    print("airflow uninstalled")
