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

# Requirements

 - [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
 - [helm](https://helm.sh)

# Configuration

Avionix airflow is configured by using Options objects, there are currently 4
 different objects:
 
1. AirflowOptions
2. PostgresOptions
3. MonitoringOptions
4. CloudOptions (Specified using LocalOptions or AwsOptions)
5. RedisOptions (Only for use with CeleryExecutor, ***not recommended***)

These options are then passed into the function *get_chart_builder*, which can be
 used to retrieve an avionix, chart builder object. For instruction on how to use the
  builder object, see [avionix](https://github.com/zbrookle/avionix)

## FAQ

- How do I change the grafana dashboard?
    - You can change the dashboard by setting the MonitoringOptions role to "Admin"