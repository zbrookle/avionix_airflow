from pathlib import Path

from avionix.testing import kubectl_get
import pytest

from avionix_airflow.kubernetes.airflow import AirflowOptions


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


def parse_shell_script(script_loc: str):
    with open(script_loc) as file:
        commands = [f"{line.strip()};" for line in file.readlines()]
        return " ".join(commands)


def skip_if_not_celery(airflow_options: AirflowOptions):
    if not airflow_options.in_celery_mode:
        pytest.skip("This functionality is only available with the celery executor")


dag_copy_loc = Path(__file__).parent / "sync_dags.sh"
