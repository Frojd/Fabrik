### Frojd Fabric - Deploy Wrapper ###
# Deployment wrapper for Frojd-Fabric, that simplifies commands running outside virtualenv

VERSION = 1

# Usage:
#   make deploy
# You can also target a specific environment:
#   make deploy FABRIC_ENV=prod

# The fabric environment you want to deploy
FABRIC_ENV = demo

# Absolute path to project
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

deploy:
	$(ROOT_DIR)/venv/bin/python $(ROOT_DIR)/venv/bin/fab $(FABRIC_ENV) deploy -c $(ROOT_DIR)/fabricrc.txt
