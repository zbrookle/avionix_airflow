from avionix_airflow.kubernetes.monitoring.elasticsearch.elasticsearch_orchestrator import (
    ElasticsearchOrchestrator,
)
from avionix_airflow.kubernetes.monitoring.grafana.grafana_orchestrator import (
    GrafanaOrchestrator,
)
from avionix_airflow.kubernetes.monitoring.telegraf.telegraf_orchestrator import (
    TelegrafOrchestrator,
)
from avionix_airflow.kubernetes.orchestration import Orchestrator


class MonitoringOrchestrator(Orchestrator):
    def __init__(self):
        orehestrator = (
            GrafanaOrchestrator() + ElasticsearchOrchestrator() + TelegrafOrchestrator()
        )
        super().__init__(orehestrator.get_kube_parts())
