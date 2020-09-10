Avionix Airflow
===============

.. image:: https://github.com/zbrookle/avionix_airflow/workflows/CI/badge.svg?branch=master
    :target: https://github.com/zbrookle/avionix_airflow/actions?query=workflow

Why are there so many guides on how to set up `Apache Airflow`_ when the code could
just be given to you?!

.. _Apache Airflow: https://airflow.apache.org
 
Welcome to ``Avionix Airflow``, an out of the box solution to installing airflow on
Kubernetes_.

.. _Kubernetes: https://kubernetes.io
 
Currently supported platforms are Minikube_ and `AWS EKS`_ (managed nodegroups only),
pull requests adding support for GKE and AKS are welcome.

.. _Minikube: https://minikube.sigs.k8s.io/docs/
.. _AWS EKS: https://aws.amazon.com/eks/
 
Overview of Avionix Airflow Capabilities
----------------------------------------

``Avionix airflow`` provides the following out of the box solutions for airflow

1. Airflow Webserver and Scheduler with configured RBAC for the KubernetesExecutor
2. Airflow metric collection (statsd -> telegraf -> elasticsearch)
3. Airflow log collection (stdout -> filebeat -> elasticsearch)
4. Metric and log visualization (elasticsearch & postgres -> grafana)

Installation
------------

.. code-block::

    pip install avionix_airflow


Requirements
------------

- kubectl_
- helm_

.. _helm: https://helm.sh
.. _kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl/

Configuration
-------------

``Avionix airflow`` is configured by using Options objects, there are currently 4
different objects:
 
1. AirflowOptions
2. PostgresOptions
3. MonitoringOptions
4. CloudOptions (Specified using LocalOptions or AwsOptions)
5. RedisOptions (Only for use with CeleryExecutor, ***not recommended***)

These options are then passed into the function *get_chart_builder*, which can be
used to retrieve an avionix_ chart builder object. For instruction on how to use the
builder object, see avionix_

.. _avionix: https://github.com/zbrookle/avionix

FAQ
---

- How do I change the grafana dashboard?
    - You can change the dashboard by setting the MonitoringOptions role to "Admin"
    
Documentation
-------------

Additional documentation can be found `here <https://avionix-airflow.readthedocs.io/en/latest/>`__