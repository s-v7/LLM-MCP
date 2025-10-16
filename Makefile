
.PHONY: setut seed run-server run-client test fmt

setup:
	python -m venv .venv  && . ./venv/bin/activate && pip install -U pip && pip install -e .
seed:
	. ./venv/bin/activate && python -m cars_arq.data_fake_c2s.py

run-server:
	. .venv/bin/activate && python -m cars_arq.server_c2s.py

run-client:
	. .venv/bin/activate && python -m cars_arq.client

test:
	. .venv/bin/activate && pytest

fmt:
	@echo "(Opcional) Use ruff/black se quiser adicionar"

