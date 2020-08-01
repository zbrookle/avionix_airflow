from avionix_airflow.kubernetes.orchestration import Orchestrator


class GrafanaOrchestrator(Orchestrator):
    def __init__(self):
        super().__init__([])
