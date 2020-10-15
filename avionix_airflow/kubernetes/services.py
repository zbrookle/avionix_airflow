from typing import Dict, Optional

from avionix.kube.core import Service, ServicePort, ServiceSpec

from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowService(Service):
    def __init__(
        self,
        name: str,
        port: int,
        target_port: int,
        node_port: int,
        selector_labels: dict,
        external_name: Optional[str] = None,
        port_name: Optional[str] = None,
        protocol: Optional[str] = None,
        node_ports_open: bool = False,
        service_type: str = "ClusterIP",
        annotations: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            AirflowMeta(name, annotations=annotations),
            ServiceSpec(
                [
                    ServicePort(
                        name=port_name,
                        port=port,
                        target_port=target_port,
                        node_port=node_port if node_ports_open else None,
                        protocol=protocol,
                    )
                ],
                selector=selector_labels,
                external_name=external_name,
                type="NodePort" if node_ports_open else service_type,
                external_traffic_policy="Local" if node_ports_open else None,
            ),
        )

    @property
    def kube_dns_name(self):
        return f"{self.metadata.name}.{self.metadata.namespace}.svc.cluster.local"


class ServiceFactory:
    _JOB_KEY = "pod-job"

    def __init__(self, namespace: str, pod_namespace: str, sql_options: SqlOptions):
        self._namespace = namespace
        self._pod_namespace = pod_namespace
        self._sql_options = sql_options
        self._values = ValueOrchestrator()

    @property
    def database_service(self) -> AirflowService:
        return AirflowService(
            self._sql_options.POSTGRES_HOST,
            self._sql_options.POSTGRES_PORT,
            target_port=self._sql_options.POSTGRES_PORT,
            node_port=30001,
            selector_labels=self._values.database_labels,
            node_ports_open=True,
        )
