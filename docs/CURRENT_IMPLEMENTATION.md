# Current Implementation

The current working implementation is located in:

src/cars_arq/

## Main files

- client_c2s.py — terminal client
- server_c2s.py — server process
- db_c2s.py — SQLite access
- data_fake_c2s.py — fake data generator
- models_c2s.py — car data model
- protocol_mcp_c2s.py — protocol layer
- configs.py — configuration

## Current database

cars.db

## Current tests

- tests/test_filters.py
- tests/test_db_filters_integration.py
- tests/test_nl_parse.py
- tests/test_rtp.py

## Refactoring rule

Do not move or rename the working source code before tests are stable.

Every structural change must be small and followed by:

pytest -q
