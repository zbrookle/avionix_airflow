from avionix.testing import kubectl_get


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
