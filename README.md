# Desafio Técnico — Desenvolvedor Python | C2S

Este projeto implementa um **agente virtual interativo** que auxilia usuários a encontrar automóveis conforme seus filtros (marca, tipo, combustível, preço, ano etc.).  
A aplicação utiliza **comunicação cliente-servidor via protocolo MCP (Model Context Protocol)** e roda totalmente no **terminal**.

---

## Objetivo

Demonstrar domínio de **Python**, **comunicação entre processos**, **modelagem de dados**, e **boas práticas de código**, incluindo testes automatizados e clareza estrutural.

---

## Estrutura do Projeto
```bash
LLM-MCP/
├── cars.db                # Banco SQLite com veículos fictícios
├── Makefile               # Comandos utilitários (tests, run, etc.)
├── pyproject.toml         # Metadados e dependências
├── requirements.txt       # Dependências do projeto
├── README.md              # Este arquivo
├── src/
│   └── cars_arq/
│       ├── client_c2s.py        # Cliente interativo (interface no terminal)
│       ├── server_c2s.py        # Servidor MCP que acessa o banco
│       ├── db_c2s.py            # Conexão e consultas SQLite
│       ├── data_fake_c2s.py     # Geração de dados falsos com Faker
│       ├── models_c2s.py        # Modelo de dados do automóvel
│       ├── protocol_mcp_c2s.py  # Implementação do protocolo MCP
│       ├── configs.py           # Configurações gerais do sistema
│       └── __init__.py
└── tests/
        ├── test_filters.py  # Testes de filtros e consultas
        └── test_rtp.py      # Testes do protocolo de comunicação
```
---

## Instalação e Execução

### Clone o repositório
```bash
git clone https://github.com/seu-usuario/LLM-MCP.git
cd LLM-MCP
```

### Crie um ambiente virtual (se necessário)
```bash
python3 -m venv nome_ambiente
source nome_ambiente/bin/activate
```

### Instale as dependências
```bash
pip install -r requirements.txt
```

### Gere dados fictícios
```bash
python3 -m cars_arq.data_fake_c2s
```

### Inicie o servidor
```bash
python3 -m cars_arq.server_c2s
```

### Inicie o cliente
```bash
python3 -m cars_arq.client_c2s
```
