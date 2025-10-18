.PHONY: setup seed run-server run-client test fmt

VENV := .venv
PY   := python3

setup:
	$(PY) -m venv $(VENV) && . $(VENV)/bin/activate && pip install -U pip && pip install -e .

seed:
	. $(VENV)/bin/activate && $(PY) -m cars_arq.data_fake_c2s

run-server:
	. $(VENV)/bin/activate && $(PY) -m cars_arq.server_c2s

run-client:
	. $(VENV)/bin/activate && $(PY) -m cars_arq.client_c2s

test:
	. $(VENV)/bin/activate && pytest -q

fmt:
	@echo "(Opcional) Use ruff/black se quiser adicionar)"
