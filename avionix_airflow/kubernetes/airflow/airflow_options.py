class AirflowOptions:
    """
    Class for storing airflow options
    """

    def __init__(
        self,
        dag_storage: str = "50Mi",
        logs_storage: str = "50Mi",
        default_executor_cpu: int = 5,
        default_executor_memory: int = 2,
    ):
        self.dag_storage = dag_storage
        self.log_storage = logs_storage
        self.default_executor_cpu = default_executor_cpu
        self.default_executor_memory = default_executor_memory
