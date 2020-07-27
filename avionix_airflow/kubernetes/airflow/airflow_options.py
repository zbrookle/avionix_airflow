from typing import List, Optional


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
        default_executor_cpu: int = 5,
        default_executor_memory: int = 2,
        access_modes: Optional[List[str]] = None,
    ):
        self.dag_storage = dag_storage
        self.log_storage = logs_storage
        self.default_executor_cpu = default_executor_cpu
        self.default_executor_memory = default_executor_memory
        self.access_modes = self.__get_access_modes(access_modes)
        self.dag_sync_image = dag_sync_image
        self.dag_sync_command = dag_sync_command
        self.dag_sync_schedule = dag_sync_schedule

    @staticmethod
    def __get_access_modes(access_modes: Optional[List[str]]):
        if access_modes is None:
            return ["ReadWriteMany"]
        return access_modes
