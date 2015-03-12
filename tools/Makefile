### Frojd Fabric - Deploy Wrapper ###
# Deployment wrapper for Frojd-Fabric, that simplifies commands running outside virtualenv

# You can setup this using this one line command:
#   curl -L https://raw.githubusercontent.com/Frojd/Frojd-Fabric/develop/tools/Makefile > ./Makefile

VERSION = 1.1

# Usage:
#   make deploy
# You can also target a specific environment:
#   make deploy FABRIC_ENV=prod
# Use agent_deploy if you need to run ssh-agent:
#   make agent_deploy FABRIC_ENV=prod

# The fabric environment you want to deploy
FABRIC_ENV = demo

# Absolute path to project
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# Start ssh agent
ssh_agent := eval `ssh-agent -s` && ssh-add ~/.ssh/id_rsa

# Fabric Deploy
fab_deploy := $(ROOT_DIR)/venv/bin/python $(ROOT_DIR)/venv/bin/fab $(FABRIC_ENV) deploy -c $(ROOT_DIR)/fabricrc.txt

agent_deploy:
	$(ssh_agent) && $(fab_deploy)

deploy:
	$(fab_deploy)
