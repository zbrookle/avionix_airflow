import pytest
import requests

from avionix_airflow.tests.markers import celery_only_test, network_test


@pytest.fixture
def domain():
    return "http://www.avionix-airflow.com"


class Request502Error(Exception):
    pass


def try_url_connection(domain: str, path: str, expected_text: str):
    request_url = f"{domain}/{path}"
    response = requests.get(request_url)
    if response.status_code == 502:
        raise Request502Error
    assert expected_text in response.text


@network_test
def test_airflow_connection(domain):
    try_url_connection(domain, "airflow", "<title>Airflow - DAGs</title>")


@celery_only_test
@network_test
def test_flower_connection(domain):
    try_url_connection(domain, "flower/", "<title>Flower</title>")
