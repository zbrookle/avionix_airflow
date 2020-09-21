from avionix.kube.core import Secret

from avionix_airflow.kubernetes.airflow.airflow_options import AirflowOptions
from avionix_airflow.kubernetes.namespace_meta import AirflowMeta
from avionix_airflow.kubernetes.postgres import SqlOptions
from avionix_airflow.kubernetes.redis import RedisOptions
from avionix_airflow.kubernetes.value_handler import ValueOrchestrator


class AirflowSecret(Secret):
    def __init__(
        self,
        sql_options: SqlOptions,
        airflow_options: AirflowOptions,
        redis_options: RedisOptions,
    ):
        data = {
            "AIRFLOW_CONN_POSTGRES_BACKEND": sql_options.sql_uri,
            "AIRFLOW__CORE__FERNET_KEY": airflow_options.fernet_key,
            "AIRFLOW__CORE__SQL_ALCHEMY_CONN": sql_options.sql_alchemy_conn_string,
            "AIRFLOW__CELERY__RESULT_BACKEND": sql_options.sql_alchemy_conn_string,
            "AIRFLOW__CELERY__BROKER_URL": redis_options.redis_connection_string,
        }
        if airflow_options.smtp_notification_options:
            data[
                "AIRFLOW__SMTP__SMTP_PASSWORD"
            ] = airflow_options.smtp_notification_options.smtp_password
        if airflow_options.git_ssh_key:
            data["gitSshKey"] = airflow_options.git_ssh_key
        values = ValueOrchestrator()
        super().__init__(AirflowMeta(values.secret_name), string_data=data)
