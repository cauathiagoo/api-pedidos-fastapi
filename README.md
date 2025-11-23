# 📦 api-pedidos-fastapi

API completa para gerenciamento de pedidos utilizando **FastAPI**, **JWT Authentication**, **SQLAlchemy**, **Pydantic** e **SQLite**.

Este projeto simula um sistema de pedidos (como pizzaria, delivery ou restaurante), permitindo criar usuários, realizar login, criar pedidos, adicionar itens, remover, cancelar e listar pedidos, tudo com autenticação segura via JWT.

---

## 📸 Interface – Swagger UI

![alt text](image.png)

---

## 🚀 Sobre o Projeto

O objetivo deste projeto é estudar e praticar desenvolvimento backend com FastAPI, aplicando boas práticas de API REST com:

- Autenticação via JWT
- Rotas protegidas
- Organização modular (auth, pedidos)
- Padrão controller → service → router
- Documentação automática com Swagger
- Persistência com SQLite

---

## 🛠 Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **Uvicorn**
- **Passlib** (hash)
- **JWT (Json Web Token)**
- **SQLite**

---

## 📁 Estrutura do Projeto

- `main.py` → Arquivo principal que inicializa a aplicação FastAPI
- `database.py` → Configuração do banco de dados (SQLite + SQLAlchemy)
- `models.py` → Modelos do banco (ORM)
- `requirements.txt` → Lista de dependências do projeto
- `README.md` → Documentação completa do projeto(essa que vc tá lendo)

- `auth/` → Módulo responsável por autenticação

  - `controller.py` → Lógica de regras e processamento
  - `service.py` → Funções internas de regra de negócio
  - `router.py` → Rotas relacionadas a login, criação de conta e refresh token

- `pedidos/` → Módulo responsável pelo sistema de pedidos
  - `controller.py` → Controla a manipulação e fluxo dos pedidos
  - `service.py` → Regras internas (criar pedido, adicionar item, remover, etc.)
  - `router.py` → Rotas relacionadas aos pedidos e seus itens

## 🧩 Endpoints Principais

### 🔐 Autenticação ( `/auth` )

| Método | Rota              | Descrição                      |
| ------ | ----------------- | ------------------------------ |
| POST   | /auth/criar_conta | Cria um novo usuário           |
| POST   | /auth/login       | Gera tokens (access + refresh) |

---

### 🛒 Pedidos ( `/pedidos` )

| Método | Rota                                   | Descrição                         |
| ------ | -------------------------------------- | --------------------------------- |
| POST   | /pedidos/pedido                        | Cria um novo pedido               |
| GET    | /pedidos/pedido/{id}                   | Lista um pedido específico        |
| POST   | /pedidos/pedido/adicionar-item/{id}    | Adiciona um item ao pedido        |
| DELETE | /pedidos/pedido/remover-item/{id_item} | Remove um item                    |
| PUT    | /pedidos/pedido/cancelar/{id}          | Cancela o pedido                  |
| GET    | /pedidos                               | Lista todos os pedidos do usuário |

## 🗃️ Modelo do Banco de Dados

A estrutura atual utiliza SQLAlchemy ORM:

### Tabela: `usuarios`

- id
- nome
- email
- senha (hash)
- ativo
- admin

### Tabela: `pedidos`

- id
- id_usuario
- data_criacao
- status

### Tabela: `itens_pedido`

- id
- id_pedido
- sabor
- tamanho
- quantidade
- preco_unitario

## ⚙️ Como Executar o Projeto

Clone o repositório:

```bash
git clone https://github.com/cauathiagoo/api-pedidos-fastapi.git

cd api-pedidos-fastapi
```

Crie o ambiente virtual:

```
python -m venv venv
```

Ative o ambiente:

- Windows

```
venv\Scripts\activate
```

- Linux/Mac

```
source venv/bin/activate
```

Instale as dependências:

```
pip install -r requirements.txt
```

Execute o servidor:

```
uvicorn main:app --reload
```

Acesse no navegador:

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Autenticação (JWT)

A API usa autenticação **Bearer Token (JWT)**.

Fluxo de autenticação:

1. Criar usuário → `/auth/criar_conta`
2. Fazer login → `/auth/login`
3. Copiar o **access_token** retornado
4. Username e senha em _Authorize_ no Swagger
5. Clicar em Authorize

---

## 🧑‍💻 Autor

Desenvolvido por [Cauã Thiago](https://cauathiago.netlify.app/)  
Freelancer & Dev Backend

📬 Contato:  
https://github.com/cauathiagoo
