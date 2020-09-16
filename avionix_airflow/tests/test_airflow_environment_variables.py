from subprocess import check_output

import pytest


def get_name_value(var: str):
    equal_pos = var.find("=")
    after_equal = equal_pos + 1
    return var[:equal_pos], var[after_equal:]


@pytest.fixture
def airflow_environment():
    env_var_text = check_output(
        "kubectl exec -it "
        "deployment.apps/airflow-master-deployment printenv -n "
        "airflow".split(" ")
    ).decode("utf-8")
    var_dict = {}
    for var in env_var_text.split("\n"):
        name, value = get_name_value(var)
        var_dict[name] = value
    return var_dict


def test_environment_variable_values(
    airflow_options, sql_options, redis_options, airflow_environment
):
    assert (
        sql_options.sql_alchemy_conn_string
        == airflow_environment["AIRFLOW__CORE__SQL_ALCHEMY_CONN"]
    )
    assert (
        redis_options.redis_connection_string
        == airflow_environment["AIRFLOW__CELERY__BROKER_URL"]
    )

    assert (
        sql_options.sql_alchemy_conn_string
        == airflow_environment["AIRFLOW__CELERY__RESULT_BACKEND"]
    )

    assert (
        airflow_options.core_executor == airflow_environment["AIRFLOW__CORE__EXECUTOR"]
    )

    assert (
        airflow_options.default_timezone
        == airflow_environment["AIRFLOW__CORE__DEFAULT_TIMEZONE"]
    )

    assert (
        airflow_options.fernet_key == airflow_environment["AIRFLOW__CORE__FERNET_KEY"]
    )
