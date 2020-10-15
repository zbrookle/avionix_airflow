from typing import Dict, Optional

from avionix.kube.core import Service, ServicePort, ServiceSpec

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.cloud.cloud_options import CloudOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowService(Service):
    def __init__(
        self,
        name: str,
        namespace: str,
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
            AirflowMeta(name, annotations=annotations, namespace=namespace),
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


class MasterNodeService(AirflowService):
    def __init__(
        self,
        name: str,
        namespace: str,
        port: int,
        node_port: int,
        values: ValueOrchestrator,
        node_ports_open: bool,
        port_name: str = "http",
        protocol: Optional[str] = None,
        service_type: str = "ClusterIP",
        annotations: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            name,
            namespace,
            port,
            port,
            node_port,
            values.master_node_labels,
            port_name=port_name,
            protocol=protocol,
            node_ports_open=node_ports_open,
            service_type=service_type,
            annotations=annotations,
        )


class ServiceFactory:
    def __init__(
        self,
        sql_options: SqlOptions,
        cloud_options: CloudOptions,
        airflow_options: AirflowOptions,
    ):
        self._namespace = airflow_options.namespace
        self._pod_namespace = airflow_options.pods_namespace
        self._sql_options = sql_options
        self._cloud_options = cloud_options
        self._airflow_options = airflow_options
        self._values = ValueOrchestrator()

    @property
    def database_service(self) -> AirflowService:
        return AirflowService(
            self._sql_options.POSTGRES_HOST,
            self._namespace,
            self._sql_options.POSTGRES_PORT,
            target_port=self._sql_options.POSTGRES_PORT,
            node_port=30001,
            selector_labels=self._values.database_labels,
            node_ports_open=True,
        )

    @property
    def webserver_service(self) -> MasterNodeService:
        return MasterNodeService(
            "webserver-svc",
            self._namespace,
            8080,
            30000,
            self._values,
            self._airflow_options.open_node_ports,
            port_name="webserver-port",
            service_type=self._cloud_options.service_type,
            annotations=self._cloud_options.webserver_service_annotations,
        )

    @property
    def statsd_service(self) -> MasterNodeService:
        return MasterNodeService(
            "statsd",
            self._namespace,
            8125,
            30004,
            self._values,
            self._airflow_options.open_node_ports,
            port_name="statsd",
            protocol="UDP",
        )

    @property
    def flower_service(self) -> MasterNodeService:
        return MasterNodeService(
            "flower-svc",
            self._namespace,
            5555,
            30003,
            self._values,
            self._airflow_options.open_node_ports,
            port_name="flower-port",
            service_type=self._cloud_options.service_type,
        )
