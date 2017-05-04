PYTHON = python3.6
ACTIVATE = . ./venv/bin/activate;

.PHONY: help
.DEFAULT_GOAL: help

help:
	@echo "These are public command list (\`・ω・´)"
	@grep -E '^[a-zA-Z_%-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: clean_venv ## Cleaning up your environment

setup: install install_dev ## Setup environment

test: lint ## Testing

# local venv
clean_venv:
	rm -rf venv

venv:
	$(PYTHON) -m venv venv

install: venv
	$(ACTIVATE) pip install -r requirements.txt -c constraints.txt

install_dev: venv
	$(ACTIVATE) pip install -r requirements-dev.txt -c constraints.txt

freeze: venv  ## Freeze pip modules into constraints.txt
	$(ACTIVATE) pip freeze > constraints.txt

lint: venv  ## Linting your scripts
	$(ACTIVATE) flake8 blog *.py
	$(ACTIVATE) mypy --ignore-missing-import --strict blog *.py

build: venv lint  ## Build your blog
	$(ACTIVATE) python build.py

preview:  ## Run nginx for preview
	docker run --name nginx -p 80:80 -v $(CURDIR)/__dist:/usr/share/nginx/html -it --rm nginx:mainline-alpine

deploy: venv ## Deploy to GitHub
	$(ACTIVATE) python deploy.py
