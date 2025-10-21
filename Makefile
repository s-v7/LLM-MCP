.PHONY: setup seed run-server run-client test fmt build-retrain run-retrain logs-retrain release changelog

VENV := .venv
PY   := python3
IMG=llm-mcp-retrain:latest
ART=/opt/llm-mcp/artifacts


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

build-retrain:
	docker build -f docker/retrain.Dockerfile -t $(IMG)

run-retrain:
	mkdir -p $(ART)
docker run --rm -v $(ART):/artifacts -e ARTIFACT_DIR/artifacts $(IMG)

logs-retrain:
	journalctl -u retrain.service -n 200 -f

changelog: 
	npx auto-changelog --commit-limit false --template keepachangelog --output CHANGELOG.md

release:
	git push origin --tags
