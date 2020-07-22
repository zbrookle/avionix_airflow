from subprocess import check_output
from typing import Optional
from logging import info
from pathlib import Path

def build_airflow_docker_image(path_to_dockerfile: Optional[str] = None):
    if path_to_dockerfile is None:
        path_to_dockerfile = str(Path(__file__).parent)
    output = check_output(["docker", "build", path_to_dockerfile])
    info(output)