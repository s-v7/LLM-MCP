<h1 align="center">LLM-MCP — Agente Virtual Interativo para Busca de Automóveis</h1>
<p align="center">
  <em>Talk to your car database — natural language meets data intelligence.</em><br>
  <a href="https://www.sv7analytics.com.br" target="_blank"><strong>sv7analytics.com.br</strong></a>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python 3.12+"></a>
  <a href="https://pypi.org/project/pytest/"><img src="https://img.shields.io/badge/tests-pytest%20✔-brightgreen" alt="pytest"></a>
  <a href="https://www.sqlite.org/"><img src="https://img.shields.io/badge/database-SQLite-lightgrey.svg" alt="SQLite"></a>
  <a href="https://faker.readthedocs.io/"><img src="https://img.shields.io/badge/data-Faker-yellow.svg" alt="Faker"></a>
  <a href="https://modelcontextprotocol.io/"><img src="https://img.shields.io/badge/protocol-MCP-orange.svg" alt="Model Context Protocol"></a>
</p>

---

##  Sobre o projeto

**LLM-MCP** é um agente virtual interativo para busca de automóveis usando linguagem natural.
  Ferramenta demonstrativa em **Python** que oferece um **agente virtual** para busca interativa de automóveis diretamente no terminal.  O projeto utiliza **arquitetura cliente-servidor** baseada no **protocolo MCP (Model Context Protocol)**, com **armazenamento SQLite**, **geração automática de dados fictícios** e uma **suíte de testes automatizados** para demonstrar integração inteligente entre NLP e bancos de dados estruturados.

---

## Objetivo

Demonstrar domínio de:
- **Python moderno (3.12+)**
- **Comunicação entre processos (cliente ↔ servidor)**
- **Modelagem e persistência de dados**
- **Boas práticas de código**
- **Testes automatizados e legibilidade estrutural**

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

### Tests Automatizados
```bash
pytest -v
|| Via Makefile
make test
```
---
## Makefile (atalhos)

Os principais comandos estão disponíveis via `make`:

| Comando          | O que faz                                                                 |
|------------------|---------------------------------------------------------------------------|
| `make setup`     | Cria `.venv`, atualiza `pip` e instala o pacote em modo editável          |
| `make seed`      | Gera/atualiza os dados fictícios no `cars.db`                             |
| `make run-server`| Sobe o servidor MCP                                                       |
| `make run-client`| Abre o cliente interativo (CLI)                                           |
| `make test`      | Roda a suíte de testes (`pytest -q`)                                      |
| `make fmt`       | Formatação/lint (opcional — ver notas abaixo)                             |

> Dica de fluxo: `make setup && make seed && make run-server` (num terminal) e `make run-client` (em outro).

---

### Os testes verificam 
- Filtros de busca e coerência dos resultad
- Comunicação correta entre cliente e servidor via MCP.
- Respostas esperadas do agente em interações simuladas.

---

### Exemplos de Consultas CLI
- **preço até 70.000**
- **sedan flex entre 2018 e 2020**
- **SUV a diesel em SP**
- **quero hvr 2023**
- **picape elétrica até 120 mil**

---

### Tecnologias Utilizadas
- **Python 3.12+**
- **SQLite/SQLAlchemy**
- **Faker (dados fic..)**
- **pytest**
- **PrettyTable (Formatação de resultados no terminal)**
- **MCP Protocol (Model Context Protocol)**

---

### Author
**Author:** [Silas Vasconcelos]  
**Engineer:** Full Stack Developer 

