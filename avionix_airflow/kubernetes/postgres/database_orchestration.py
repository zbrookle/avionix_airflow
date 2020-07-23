from avionix_airflow.kubernetes.orchestration import Orchestrator
from avionix_airflow.kubernetes.postgres.database_deployment import DatabaseDeployment
from avionix_airflow.kubernetes.postgres.database_service import DatabaseService
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions


class PostgresOrchestrator(Orchestrator):
    def __init__(self, sql_options: SqlOptions):
        super().__init__(
            [DatabaseDeployment(sql_options), DatabaseService(sql_options)]
        )
