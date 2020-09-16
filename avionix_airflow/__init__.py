# flake8: noqa
from avionix_airflow.build_airflow import get_chart_builder
from avionix_airflow.docker._build_image import build_airflow_image
from avionix_airflow.host_settings import add_host
from avionix_airflow.kubernetes.airflow import AirflowOptions, SmtpNotificationOptions
from avionix_airflow.kubernetes.cloud import AwsOptions, CloudOptions
from avionix_airflow.kubernetes.monitoring import MonitoringOptions
from avionix_airflow.kubernetes.postgres import SqlOptions
from avionix_airflow.kubernetes.redis import RedisOptions

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
