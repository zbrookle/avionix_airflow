from avionix import ChartBuilder, ChartInfo
from avionix_airflow.docker.build_image import build_airflow_docker_image
from kubernetes import AirflowNamespace, AirflowDeployment
from avionix.errors import ChartAlreadyInstalledError


def get_chart_builder():
    builder = ChartBuilder(
        ChartInfo(
            api_version="3.2.4", name="airflow", version="0.1.0", app_version="v1"
        ),
        [AirflowNamespace(), AirflowDeployment()],
    )
    return builder


def install_chart():
    build_airflow_docker_image()
    get_chart_builder().install_chart()


def uninstall_chart():
    get_chart_builder().uninstall_chart()


def main():
    try:
        install_chart()
    except ChartAlreadyInstalledError:
        uninstall_chart()
        install_chart()


if __name__ == "__main__":
    main()
