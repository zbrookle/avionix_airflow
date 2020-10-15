from avionix.kube.core import Secret

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.postgres import SqlOptions
from avionix_airflow.kubernetes.redis import RedisOptions
from avionix_airflow.kubernetes.services import ServiceFactory
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowSecret(Secret):
    def __init__(
        self,
        sql_options: SqlOptions,
        airflow_options: AirflowOptions,
        redis_options: RedisOptions,
        namespace: str,
        service_factory: ServiceFactory,
    ):
        sql_conn_string = sql_options.get_sql_alchemy_conn_string(
            service_factory.database_service.kube_dns_name
        )
        data = {
            "AIRFLOW_CONN_POSTGRES_BACKEND": sql_options.get_sql_uri(
                service_factory.database_service.kube_dns_name
            ),
            "AIRFLOW__CORE__FERNET_KEY": airflow_options.fernet_key,
            "AIRFLOW__CORE__SQL_ALCHEMY_CONN": sql_conn_string,
            "AIRFLOW__CELERY__RESULT_BACKEND": sql_conn_string,
            "AIRFLOW__CELERY__BROKER_URL": redis_options.redis_connection_string,
        }
        if airflow_options.smtp_notification_options:
            data[
                "AIRFLOW__SMTP__SMTP_PASSWORD"
            ] = airflow_options.smtp_notification_options.smtp_password
        if airflow_options.git_ssh_key:
            data["gitSshKey"] = airflow_options.git_ssh_key
        values = ValueOrchestrator()
        super().__init__(
            AirflowMeta(values.secret_name, namespace=namespace), string_data=data
        )
