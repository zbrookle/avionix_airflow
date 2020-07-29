from python_hosts import Hosts, HostsEntry
from avionix_airflow.kubernetes.airflow import AirflowOptions
from avionix_airflow.kubernetes.utils import get_minikube_ip
import os

class HostWriteContext:

    def __init__(self, hosts: Hosts):
        self._hosts = hosts
        self._permission_state = 0

    def __enter__(self):
        print(os.stat(self._hosts.determine_hosts_path()))
        exit()
        os.chmod(self._hosts.determine_hosts_path(), 777)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("switching back permissions")


def add_host(
    airflow_options: AirflowOptions,
    entry_type: str = "ipv4",
    address: str = get_minikube_ip(),
):
    with HostWriteContext(Hosts()) as hosts:
        exit()
        my_hosts = Hosts()
        my_hosts.add(
            [HostsEntry(entry_type, address=address, names=airflow_options.domain_name)]
        )
        path = my_hosts.determine_hosts_path()
        print()
        my_hosts.write()