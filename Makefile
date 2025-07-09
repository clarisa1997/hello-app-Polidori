# Makefile

PY_IMAGE := python:3.11-slim
WORKDIR  := /app

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

## Lint all Python code using flake8 inside Docker
lint:
	docker run --rm \
	  -v "$(PWD)":$(WORKDIR) \
	  -w $(WORKDIR) \
	  $(PY_IMAGE) \
	  bash -c "\
	    pip install --upgrade pip && \
		pip install flake8 && \
	    flake8 backend frontend tests || echo "flake8 ha rilevato errori"\
	  "

## Run full test suite (unit + e2e) inside Docker
test:
	docker run --rm \
	  --network host \
	  -v "$(PWD)":$(WORKDIR) \
	  -w $(WORKDIR) \
	  -e PYTHONPATH=$(WORKDIR) \
	  $(PY_IMAGE) \
	  bash -c "\
	    pip install --upgrade pip && \
	    pip install -r backend/requirements.txt \
	                -r frontend/requirements.txt \
	                -r tests/requirements.txt && \
	    pytest -q \
	  "

.PHONY: build up down logs lint test
