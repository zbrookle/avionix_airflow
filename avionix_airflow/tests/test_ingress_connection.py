import requests
import pytest


@pytest.fixture
def domain():
    return "http://www.avionix-airflow.com"


class Request502Error(Exception):
    pass


@pytest.mark.parametrize(
    "path,expected_text",
    [("airflow", "<title>Airflow - DAGs</title>"), ("flower/", "I'm flower")],
)
@pytest.mark.flaky
def test_url_connection(domain: str, path: str, expected_text: str):
    request_url = f"{domain}/{path}"
    response = requests.get(request_url)
    if response.status_code == 502:
        raise Request502Error
    assert expected_text in response.text
