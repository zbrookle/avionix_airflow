import pytest
import requests

from avionix_airflow.tests.markers import network_test


@pytest.fixture
def domain():
    return "http://www.avionix-airflow.com"


class Request502Error(Exception):
    pass


@pytest.mark.parametrize(
    "path,expected_text",
    [
        ("airflow", "<title>Airflow - DAGs</title>"),
        ("flower/", "<title>Flower</title>"),
    ],
)
@network_test
def test_url_connection(domain: str, path: str, expected_text: str):
    request_url = f"{domain}/{path}"
    response = requests.get(request_url)
    if response.status_code == 502:
        raise Request502Error
    assert expected_text in response.text
