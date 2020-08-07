#!/bin/bash -e

# Set /etc/hosts to writable for testing
sudo chmod 646 /etc/hosts

export SHELL=/bin/bash
pytest --log-cli-level info --log-format "[%(filename)s:%(lineno)s] %(message)s"