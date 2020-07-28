from avionix.kubernetes_objects.core import EnvVar

from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class SqlOptions:
    def __init__(
        self,
        user: str = "airflow",
        password: str = "airflow",
        host: str = ValueOrchestrator().database_service_name,
        port: int = 5432,
        db: str = "airflow",
        extras="",
    ):
        self.POSTGRES_USER = user
        self.POSTGRES_PASSWORD = password
        self.POSTGRES_HOST = host
        self.POSTGRES_PORT = port
        self.POSTGRES_DB = db
        self.POSTGRES_EXTRAS = extras

    def get_airflow_environment(self):
        return [EnvVar(name, str(self.__dict__[name])) for name in self.__dict__]

    def get_postgres_envioronment(self):
        return [
            var
            for var in self.get_airflow_environment()
            if var.name in {"POSTGRES_USER", "POSTGRES_PASSWORD"}
        ]

    @property
    def _postgres_user_host_string(self):
        return (
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def sql_alchemy_connection_string(self):
        return (
            f"postgresql+psycopg2://{self._postgres_user_host_string}"
            f"{self.POSTGRES_EXTRAS}"
        )

    @property
    def sql_uri(self):
        return f"postgres://{self._postgres_user_host_string}"
