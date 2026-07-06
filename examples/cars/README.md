# Cars MCP Example

Thi is the first working example of the LLM-MCP Lab.

It demonstrates a car search assistant using:

- Python
- SQLite
- fake vehicle data
- client-server communication
- MCP-like protocol
- automated tests

## Current implementation

The current source code is still located at:

src/cars_arq/

This will be refactored later in small steps.

## Run
Server:
python3 -m cars_arq.server_c2s
Client:
python3 -m cars_arq.client_c2s
Tests:
pytest -q


