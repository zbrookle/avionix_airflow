from typing import Dict, List, Optional

from avionix.kube.core import EnvVar
from cryptography.fernet import Fernet


def _create_fernet_key():
    return Fernet.generate_key().decode("utf-8")


class AirflowOptions:
    """
    Class for storing airflow options
    """

    def __init__(
        self,
        dag_sync_image: str,
        dag_sync_command: List[str],
        dag_sync_schedule: str,
        dag_storage: str = "50Mi",
        logs_storage: str = "50Mi",
        external_storage: str = "50Mi",
        default_executor_cpu: int = 5,
        default_executor_memory: int = 2,
        access_modes: Optional[List[str]] = None,
        default_timezone: str = "utc",
        core_executor: str = "CeleryExecutor",
        namespace: str = "airflow",
        domain_name: Optional[str] = "www.avionix-airflow.com",
        additional_vars: Optional[Dict[str, str]] = None,
        fernet_key: str = _create_fernet_key(),
        dags_paused_at_creation: bool = True,
        worker_image: str = "airflow-image",
        worker_image_tag: str = "latest",
        open_node_ports: bool = False,
        local_mode: bool = False,
    ):
        self.dag_storage = dag_storage
        self.log_storage = logs_storage
        self.external_storage = external_storage
        self.default_executor_cpu = default_executor_cpu
        self.default_executor_memory = default_executor_memory
        self.access_modes = self.__get_access_modes(access_modes)
        self.dag_sync_image = dag_sync_image
        self.dag_sync_command = dag_sync_command
        self.dag_sync_schedule = dag_sync_schedule
        self.domain_name = domain_name
        self.default_time_zone = default_timezone
        self.core_executor = core_executor
        self.namespace = namespace
        self.__additional_vars = additional_vars if additional_vars is not None else {}
        self.fernet_key = fernet_key
        self.dags_paused_at_creation = dags_paused_at_creation
        self.worker_image = worker_image
        self.worker_image_tag = worker_image_tag
        self.open_node_ports = open_node_ports
        self.local_mode = local_mode
        if worker_image == "airflow-image" and not self.local_mode:
            self.worker_image = "zachb1996/avionix_airflow"

    @staticmethod
    def __get_access_modes(access_modes: Optional[List[str]]):
        if access_modes is None:
            return ["ReadWriteMany"]
        return access_modes

    @property
    def extra_env_vars(self):
        return [EnvVar(name, value) for name, value in self.__additional_vars.items()]

    @property
    def in_celery_mode(self):
        return self.core_executor == "CeleryExecutor"

    @property
    def in_kube_mode(self):
        return self.core_executor == "KubernetesExecutor"
