from subprocess import check_call, check_output
from typing import Optional
from logging import info
from pathlib import Path
import re
import os


def build_airflow_docker_image(
    path_to_dockerfile: Optional[str] = None, minikube_mode: bool = True
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
    info("Building airflow docker image")
    check_call(["docker", "build", "-t", "airflow-image", path_to_dockerfile])
    info("Docker image built")
