#!/bin/bash -e

# Set /etc/hosts to writable for testing
sudo chmod 646 /etc/hosts

pytest
pytest KubernetesExecutor