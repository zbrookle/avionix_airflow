from avionix_airflow.kubernetes.orchestration import Orchestrator
from avionix_airflow.kubernetes.airflow.airflow_master import AirflowDeployment
from avionix_airflow.kubernetes.airflow.airflow_namespace import AirflowNamespace
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions


class AirflowOrchestrator(Orchestrator):
    def __init__(self, pg_options: SqlOptions):
        super().__init__([AirflowNamespace(), AirflowDeployment(pg_options)])
