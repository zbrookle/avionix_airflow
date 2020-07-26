from avionix_airflow.kubernetes.base_service import AirflowService
from avionix_airflow.kubernetes.label_handler import LabelHandler
from avionix_airflow.kubernetes.postgres.sql_options import SqlOptions


class DatabaseService(AirflowService):
    def __init__(self, sql_options: SqlOptions):
        label = LabelHandler()
        super().__init__(
            label.database_service_name,
            sql_options.POSTGRES_PORT,
            target_port=sql_options.POSTGRES_PORT,
            node_port=30001,
            selector_labels=label.database_labels,
        )
