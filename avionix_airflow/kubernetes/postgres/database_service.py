from avionix.kubernetes_objects.service import Service, ServiceSpec, ServicePort
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions
from avionix_airflow.kubernetes.label_handler import LabelHandler


class DatabaseService(Service):
    def __init__(self, sql_options: SqlOptions):
        label = LabelHandler()
        super().__init__(
            AirflowMeta(name="airflow-database-connection"),
            ServiceSpec(
                [
                    ServicePort(
                        sql_options.POSTGRES_PORT, target_port=sql_options.POSTGRES_PORT
                    )
                ],
                selector=label.database_labels,
                external_name=label.database_service_name,
                external_ips=[sql_options.POSTGRES_HOST]
            ),
        )
