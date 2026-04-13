# Sistema-PDV

Sistema de ponto de venda (PDV) desenvolvido em FastAPI com PostgreSQL e SQLAlchemy.

## Visão geral

Este backend oferece APIs para gestão de usuários, clientes, produtos, categorias, subcategorias, estoque, compras, vendas, fornecedores e relatórios.

## Tecnologias

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Uvicorn
- python-decouple

## Estrutura do projeto

- `main.py` — ponto de entrada da aplicação
- `src/db/` — configuração de banco e sessão
- `src/models/` — definição das entidades SQLAlchemy
- `src/routes/` — rotas da API
- `src/repository/` — lógica de persistência e operações no banco
- `src/schemas/` — schemas Pydantic para validação e respostas
- `alembic/` — migrações do banco
- `create_tables.py` — script para criar tabelas diretamente

## Requisitos

- Python 3.13
- PostgreSQL
- `pip` instalado

## Configuração

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd Sistema-PDV
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Defina a variável de ambiente `DB_URL` com a string de conexão do PostgreSQL:

```bash
export DB_URL="postgresql+psycopg2://usuario:senha@localhost:5432/nome_do_banco"
```

> O projeto usa `python-decouple`, então você também pode armazenar `DB_URL` em um arquivo `.env`.

## Banco de dados

Para criar as tabelas automaticamente a partir dos modelos:

```bash
python create_tables.py
```

Para usar migrações com Alembic:

```bash
alembic upgrade head
```

## Executando localmente

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A API ficará disponível em `http://localhost:8000`.

## Endpoints principais

A aplicação expõe rotas REST para os seguintes recursos:

- `/users` — usuários
- `/clients` — clientes
- `/products` — produtos
- `/product_categories` — categorias de produtos
- `/product_sub_categories` — subcategorias de produtos
- `/stocks` — estoque
- `/purchase` — compras
- `/sales` — vendas
- `/suppliers` — fornecedores
- `/reports` — relatórios
- `/login` — autenticação/login

### Relatórios

- `/reports/stock`
- `/reports/sales`
- `/reports/purchases`
- `/reports/sold-products`

## Documentação automática

Com o servidor em execução, a documentação interativa está disponível em:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Docker

O `Dockerfile` constrói a aplicação com Python 3.13. Para iniciar o serviço via container:

```bash
docker build -t sistema-pdv .
docker run -e DB_URL="postgresql+psycopg2://usuario:senha@host:5432/banco" -p 8000:8000 sistema-pdv
```

Também existe um `docker-compose.yml` que define serviços para PostgreSQL, pgAdmin, backend e frontend.

## Observações

- Ajuste `DB_URL` conforme o host e as credenciais do seu banco.
- Se for usar o `docker-compose`, verifique se os volumes e caminhos estão corretos para seu ambiente.
