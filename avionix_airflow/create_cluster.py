from avionix import ChartBuilder, ChartInfo
from avionix_airflow.docker.build_image import build_airflow_docker_image

def main():
    build_airflow_docker_image()
    builder = ChartBuilder(ChartInfo(
        api_version="3.2.4", name="test", version="0.1.0", app_version="v1"
    ), [])


if __name__ == '__main__':
    main()