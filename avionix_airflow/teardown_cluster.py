from logging import info

from avionix import ChartBuilder

from avionix_airflow.tests.utils import kubectl_name_dict


def teardown(builder: ChartBuilder):
    builder.uninstall_chart()
    while True:
        if not kubectl_name_dict("configmap"):
            break
    info("Terminating...")
    info("airflow uninstalled")
