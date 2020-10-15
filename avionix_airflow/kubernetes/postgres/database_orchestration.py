from avionix_airflow.kubernetes.orchestration import Orchestrator
from avionix_airflow.kubernetes.postgres.database_deployment import DatabaseDeployment
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.services import ServiceFactory


class PostgresOrchestrator(Orchestrator):
    def __init__(self, sql_options: SqlOptions, service_factory: ServiceFactory):
        super().__init__(
            [DatabaseDeployment(sql_options), service_factory.database_service]
        )
