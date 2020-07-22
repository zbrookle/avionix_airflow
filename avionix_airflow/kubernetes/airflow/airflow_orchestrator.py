from avionix_airflow.kubernetes.orchestration import Orchestrator
from avionix_airflow.kubernetes.airflow.airflow_master import AirflowDeployment
from avionix_airflow.kubernetes.airflow.airflow_namespace import AirflowNamespace


class AirflowOrchestrator(Orchestrator):

    _parts = [AirflowNamespace(), AirflowDeployment()]
