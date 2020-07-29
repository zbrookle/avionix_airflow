from python_hosts import Hosts, HostsEntry

from avionix_airflow.kubernetes.airflow import AirflowOptions
from avionix_airflow.kubernetes.utils import get_minikube_ip


def add_host(
    airflow_options: AirflowOptions,
    entry_type: str = "ipv4",
    address: str = get_minikube_ip(),
    force: bool = False,
):
    my_hosts = Hosts()
    my_hosts.add(
        [HostsEntry(entry_type, address=address, names=[airflow_options.domain_name])],
        force=force,
    )
    my_hosts.write()
