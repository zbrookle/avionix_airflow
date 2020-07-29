from logging import info
import os
from pathlib import Path
import re
from subprocess import check_output

docker_path = Path(__file__).parent


def build_docker_image(
    image_name: str, path_to_dockerfile: str, minikube_mode: bool = True,
):
    if path_to_dockerfile is None:
        path_to_dockerfile = str(Path(__file__).parent)
    if minikube_mode:
        bash_code = check_output(["minikube", "docker-env"])
        lines = bash_code.decode("utf-8").split("\n")
        export_lines = lines[:4]
        for line in export_lines:
            match = re.match(r"export (?P<var_name>.*)=\"(?P<value>.*)\"", line)
            if match:
                os.putenv(match.group("var_name"), match.group("value"))
    info(f"Building {image_name} docker image")
    check_output(["docker", "build", "-t", image_name, path_to_dockerfile])
    info("Docker image built")


def build_airflow_image():
    build_docker_image("airflow-image", str(docker_path / "airflow"))
