# Architecture — LLM-MCP Lab

## Current flow

```text
User
  │
  ▼
CLI Client
  │
  ▼
Custom MCP-like Protocol
  │
  ▼
MCP Server
  │
  ▼
SQLite Database
```

## Target flow

```text
User
  │
  ▼
LLM Client
  │
  ▼
MCP Protocol
  │
  ▼
MCP Server
  │
  ├── SQLite Tools
  ├── PostgreSQL Tools
  ├── Filesystem Tools
  ├── PDF Tools
  ├── REST API Tools
  └── RAG Tools
```

## Lab modules

| Module | Purpose |
|---------|---------|
| `examples/cars` | Automotive search example |
| `examples/products` | Product search example |
| `examples/finance` | Financial systems demo: transactions, accounts, invoices and analytics |
| `examples/employees` | Employee database example |
| `examples/pdf` | PDF extraction example |
| `examples/sql` | SQL query example |
| `examples/rag` | Retrieval-Augmented Generation example |
| `mcp_server` | MCP server implementations |
| `mcp_client` | MCP client implementations |
| `docs` | Documentation and architecture |
| `tests` | Automated tests |
