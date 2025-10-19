## LLM-MCP — Agente Virtual Interativo para Busca de Automóveis

Ferramenta demonstrativa em **Python** que oferece um **agente virtual** para busca interativa de automóveis diretamente no terminal.  
O projeto utiliza **arquitetura cliente-servidor** baseada no **protocolo MCP (Model Context Protocol)**, com **armazenamento SQLite**, **geração automática de dados fictícios** e uma **suíte de testes automatizados** para validar filtros e comunicação.

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

### Tests Automatizados
```bash
pytest -v
|| Via Makefile
make test
```

### Os testes verificam 
- Filtros de busca e coerência dos resultad
- Comunicação correta entre cliente e servidor via MCP.
- Respostas esperadas do agente em interações simuladas.

### Tecnologias Utilizadas
- **Python 3.12+**
- **SQLite/SQLAlchemy**
- **Faker (dados fic..)
- **pytest**
- **PrettyTable (Formatação de resultados no terminal)**
- **MCP Protocol (Model Context Protocol)**



### Author
**Author:** [Silas Vasconcelos]  
**Engineer:** Full Stack Developer 

