Minikube Setup
==============

For the minikube setup you will need to install `minikube <https://kubernetes
.io/docs/tasks/tools/install-minikube/>`__ and `docker <https://docs.docker
.com/get-docker/>`__.

To start minikube:

.. code-block:: bash

    minikube start --driver=docker

To start ingress controller (nginx by default):

.. code-block:: bash

    minikube addons enable ingress