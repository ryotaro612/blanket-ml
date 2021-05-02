BASE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
VENV ?= $(BASE_DIR)venv/
PYENV_FILE := $(BASE_DIR).python-version
DATASETS_DIR := $(BASE_DIR)datasets/

help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

test: $(VENV)bin/activate $(BASE_DIR).env ## Run unit tests.
	cd $(BASE_DIR) && \
	. $(VENV)bin/activate && \
	pip install --upgrade pip && \
	pip install -e .[dev] && \
	python -m unittest

clean: ## Delete unnecessary files.
	rm -rf $(VENV) $(PYENV_FILE)

all: $(DATASETS_DIR)raw_email_events$(SUFFIX).csv $(DATASETS_DIR)raw_requests$(SUFFIX).csv
	@echo

$(DATASETS_DIR)raw_email_events$(SUFFIX).csv: ## Fetch raw email events.
	. $(VENV)bin/activate && \
	beat_analytics email raw $(DATASETS_DIR)raw_email_events$(SUFFIX).csv


$(DATASETS_DIR)raw_requests$(SUFFIX).csv: ## Fetch raw requests.
	. $(VENV)bin/activate && \
	beat_analytics web raw $(DATASETS_DIR)raw_requests$(SUFFIX).csv

$(PYENV_FILE):
	cd $(BASE_DIR) && pyenv local 3.9.0

$(VENV)bin/activate: $(PYENV_FILE)
	cd $(BASE_DIR) && python -m venv $(VENV)

$(BASE_DIR).env:
	echo "RAW_EMAIL_TABLE" >> $(BASE_DIR).env
	echo "RAW_WEB_REQUEST_TABLE" >> $(BASE_DIR).env