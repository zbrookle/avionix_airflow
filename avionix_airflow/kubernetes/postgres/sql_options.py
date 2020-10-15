from typing import Optional

from avionix.kube.core import EnvVar


class SqlOptions:
    """
    Provides configuration for the airflow backend database. Currently only postgres
    is supported. Note that all connection related strings will be stored in
    kubernetes secrets on the cluster.

    :param user: The username for database
    :param password: The pass for the database
    :param host: The hostname for the database
    :param port: The port to keep open for the database
    :param db: The database name
    :param create_database_in_cluster: Whether airflow should create the database
    :param extras: Any extra params to be appended to the end of the db connection \
        string
    """

    def __init__(
        self,
        user: str = "airflow",
        password: str = "airflow",
        host: str = "airflow-database-connection",
        port: int = 5432,
        db: str = "airflow",
        create_database_in_cluster: bool = True,
        extras="",
    ):
        self.create_database_in_cluster = create_database_in_cluster
        self.POSTGRES_USER = user
        self.POSTGRES_PASSWORD = password
        self.POSTGRES_HOST = host
        self.POSTGRES_PORT = port
        self.POSTGRES_DB = db
        self.POSTGRES_EXTRAS = extras

    def get_sql_environment(self):
        return [EnvVar(name, str(self.__dict__[name])) for name in self.__dict__]

    def get_postgres_envioronment(self):
        return [
            var
            for var in self.get_sql_environment()
            if var.name in {"POSTGRES_USER", "POSTGRES_PASSWORD"}
        ]

    def _get_postgres_user_host_string(self, host: Optional[str] = None):
        if not self.create_database_in_cluster:
            host = self.POSTGRES_HOST
        return (
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{host}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def get_sql_alchemy_conn_string(self, host: Optional[str] = None):
        return (
            f"postgresql+psycopg2://{self._get_postgres_user_host_string(host)}"
            f"{self.POSTGRES_EXTRAS}"
        )

    def get_sql_uri(self, host: Optional[str] = None):
        return f"postgres://{self._get_postgres_user_host_string(host)}"
