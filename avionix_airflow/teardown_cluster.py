from logging import info

from avionix import ChartBuilder


def teardown(builder: ChartBuilder):
    builder.uninstall_chart()
    info("Terminating...")
    info("airflow uninstalled")
