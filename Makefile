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

mail_raw_email_events_file := $(DATASETS_DIR)raw_email_events$(SUFFIX).csv
mail_format_events_file := $(DATASETS_DIR)mail_format_events.csv
mail_open_free_file := $(DATASETS_DIR)mail_open_free.csv
requests_raw_file := $(DATASETS_DIR)raw_requests$(SUFFIX).csv
user_master_file := $(DATASETS_DIR)master_user.jsonl

all: $(user_master_file) $(mail_format_events_file) $(requests_raw_file) ## Create all the artifacts.
	@echo

$(mail_raw_email_events_file): ## Fetch raw email events.
	. $(VENV)bin/activate && \
	beat_analytics email raw $(mail_raw_email_events_file)

$(requests_raw_file): ## Fetch raw requests.
	. $(VENV)bin/activate && \
	beat_analytics web raw $(requests_raw_file)

$(mail_format_events_file): $(mail_raw_email_events_file)
	. $(VENV)bin/activate && \
	beat_analytics email format $(mail_raw_email_events_file) $(mail_format_events_file)

# TODO
$(mail_open_free_file): $(mail_format_events_file)
	. $(VENV)bin/activate && \
	beat_analytics email open free $(mail_format_events_file) $(mail_open_free_file)

$(user_master_file): $(DATASETS_DIR)user.tsv $(DATASETS_DIR)user_plan.tsv $(DATASETS_DIR)plan.tsv $(DATASETS_DIR)plan_history.tsv
	. $(VENV)bin/activate && \
	beat_analytics user master $(DATASETS_DIR)user.tsv $(DATASETS_DIR)user_plan.tsv $(DATASETS_DIR)plan.tsv $(DATASETS_DIR)plan_history.tsv $(user_master_file)

$(PYENV_FILE):
	cd $(BASE_DIR) && pyenv local 3.9.0

$(VENV)bin/activate: $(PYENV_FILE)
	cd $(BASE_DIR) && python -m venv $(VENV)

$(BASE_DIR).env:
	echo "RAW_EMAIL_TABLE" >> $(BASE_DIR).env
	echo "RAW_WEB_REQUEST_TABLE" >> $(BASE_DIR).env