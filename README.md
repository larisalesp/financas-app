# ꕥ Flowly

Aplicação de finanças pessoais com backend em FastAPI e frontend em React.

![Python](https://img.shields.io/badge/Python-3.11-c4728a?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-7a8c4a?style=flat&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-c4728a?style=flat&logo=mongodb&logoColor=white)
![React](https://img.shields.io/badge/React-Tailwind-7a8c4a?style=flat&logo=react&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-e8aaba?style=flat&logo=jsonwebtokens&logoColor=white)

## ‎❥ Sobre:
Desenvolvi essa aplicação como projeto de portfólio para praticar o desenvolvimento fullstack.

O projeto vai além de um CRUD simples: inclui autenticação JWT, categorias personalizadas, importação via CSV e relatórios históricos, refletindo um caso de uso real do dia a dia.

A motivação veio de uma necessidade real: querer entender para onde o dinheiro vai e ter mais controle sobre as minhas finanças pessoais.

## ‎❥ Funcionalidades:

- Autenticação com JWT
- Cadastro e login de usuários
- CRUD de transações (receitas e despesas)
- Categorias personalizadas
- Importação via CSV
- Alertas de orçamento
- Relatórios históricos

## ‎❥ Tecnologias:

**Backend**
- Python 3.11
- FastAPI + Motor (async)
- MongoDB 7
- JWT + bcrypt

**Frontend**
- React
- Tailwind CSS

## ‎❥ Estrutura do Projeto:

- `backend/` — API FastAPI
  - `app/routers/` — rotas
  - `app/models.py` — modelos Pydantic
  - `app/auth.py` — autenticação JWT
  - `app/database.py` — conexão MongoDB
  - `app/main.py` — entrada da aplicação
- `frontend/` — interface React
