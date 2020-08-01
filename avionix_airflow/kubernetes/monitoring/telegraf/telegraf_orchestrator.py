from avionix_airflow.kubernetes.orchestration import Orchestrator


class TelegrafOrchestrator(Orchestrator):
    def __init__(self):
        super().__init__([])
