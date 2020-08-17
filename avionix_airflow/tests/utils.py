from pathlib import Path
import re
from typing import Dict

from avionix.testing import kubectl_get
from pandas import DataFrame
import pytest

from avionix_airflow.kubernetes.airflow import AirflowOptions


def kubectl_get_airflow(resource: str):
    return kubectl_get(resource, "airflow")


def kubectl_name_dict(resource: str):
    info = DataFrame(kubectl_get_airflow(resource))
    info_dict: Dict[str, Dict[str, str]] = {}
    if "NAME" not in info.columns:
        return info_dict
    for name in info["NAME"]:
        filtered = info[info["NAME"] == name].reset_index()
        columns = [
            column for column in filtered.columns if column not in {"NAME", "index"}
        ]
        info_dict[name] = {column: filtered[column][0] for column in columns}
    return info_dict


def filter_out_pvc(volume_info: dict):
    return {
        volume: volume_info[volume]
        for volume in volume_info
        if not re.match("pvc-.*", volume)
    }


def parse_shell_script(script_loc: str):
    with open(script_loc) as file:
        commands = [f"{line.strip()};" for line in file.readlines()]
        return " ".join(commands)


def skip_if_not_celery(airflow_options: AirflowOptions):
    if not airflow_options.in_celery_mode:
        pytest.skip("This functionality is only available with the celery executor")


dag_copy_loc = Path(__file__).parent / "sync_dags.sh"
