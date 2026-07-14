# Changelog — LLM-MCP Lab

Todas as mudanças relevantes deste projeto são documentadas aqui.

O formato segue Semantic Versioning: MAJOR.MINOR.PATCH.

## [Unreleased] — Sprint 2: Resources & Collections

- Resource `cars://make/{make}` para consulta de veículos por fabricante
- Testes dedicados para filtro por marca e marca inexistente
- Resource `cars://model/{model}` para consulta de veículos por modelo
- Testes dedicados para modelo existente e inexistente

### Planejado
- Resource `cars://fuel/{fuel_type}`
- Resource `cars://body/{body_type}`
- Resource `cars://year/{year}`
- Resource `cars://city/{city}`
- Testes dedicados para cada Resource
- Atualização da documentação da Sprint 2

## [0.2.0] — MCP Foundation

### Adicionado

- SDK oficial Model Context Protocol
- Servidor SQLite com FastMCP
- Tool `healthcheck`
- Tool `search_cars`
- Tool `get_car`
- Resource `cars://{car_id}`
- Resource `cars://state/{state}`
- Limite seguro de até 10 resultados
- Testes automatizados para Tools, Resources e filtros
- Estrutura de laboratório com `docs`, `examples`, `mcp_server` e `mcp_client`

### Mantido

- Implementação legada em `src/cars_arq`
- Banco SQLite `cars.db`
- Cliente-servidor original
- Compatibilidade com os testes existentes

## [0.1.0] — Cars Client/Server Prototype

### Adicionado

- Cliente interativo em terminal
- Servidor Python para consulta de veículos
- Protocolo cliente-servidor customizado
- Persistência SQLite com SQLAlchemy
- Geração de dados fictícios com Faker
- Filtros por marca, modelo, ano, combustível, carroceria, preço, cidade e estado
- Testes automatizados com pytest
