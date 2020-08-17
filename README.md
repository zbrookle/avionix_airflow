# Avionix Airflow

Why are there so many guides on how to set up airflow when the code could just be
 given to you?!
 
Welcome to Avionix Airflow, an out of the box solution to installing airflow on
 kubernetes.
 
Currently supported platforms are Minikube and AWS EKS (managed nodegroups only), pull
 requests adding support for GKE and AKS are welcome.
 
# Overview of Avionix Airflow Capabilities

Avionix airflow provides the following out of the box solutions for airflow

1. Airflow Webserver and Scheduler with configured RBAC for the KubernetesExecutor
2. Airflow metric collection (statsd -> telegraf -> elasticsearch)
3. Airflow log collection (stdout -> filebeat -> elasticsearch)
4. Metric and log visualizatoin (elasticsearch & postgres -> grafana)

# Installation

```bash 
pip install avionix_airflow
```

# Setup

[kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) and [helm](https://helm.sh) are both required by the underlying package
 avionix, to interact with kubernetes

# Configuration

Avionix airflow is configured by using Options objects, there are currently 4
 different objects:
 
1. AirflowOptions
2. PostgresOptions
3. MonitoringOptions
4. CloudOptions (Specified using LocalOptions or AwsOptions)
5. RedisOptions (Only for use with CeleryExecutor, ***not reccommended***)

These options are then passed into the function *get_chart_builder*, which can be
 used to retrieve an avionix, chart builder object. For instruction on how to use the
  builder object, see [avionix](https://github.com/zbrookle/avionix)

# Usage Examples

## Minikube

```python
from avionix_airflow import add_host, build_airflow_image, get_chart_builder, AirflowOptions
from avionix_airflow.tests.utils import dag_copy_loc, parse_shell_script

TEST_AIRFLOW_OPTIONS = AirflowOptions(
    dag_sync_image="alpine/git",
    dag_sync_command=["/bin/sh", "-c", parse_shell_script(dag_copy_loc)],
    dag_sync_schedule="* * * * *",
    default_timezone="est",
    core_executor="KubernetesExecutor",
    open_node_ports=True,
)

def main():
    build_airflow_image()
    add_host(TEST_AIRFLOW_OPTIONS)
    builder = get_chart_builder(
        airflow_options=TEST_AIRFLOW_OPTIONS
    )
    builder.install_chart(options={"create-namespace": None, "dependency-update": None})
```

## AWS EKS Managed Node

```python

```


## FAQ

- How do I change the grafana dashboard?
    - You can change the dashboard by setting the MonitoringOptions role to "Admin"