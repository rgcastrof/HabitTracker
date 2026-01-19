# Habit Tracker API (MongoDB)
RestAPI de sistema de rastreamento de hábitos desenvolvido
com FastAPI, MongoDB e Beanie.

### Tecnologias utilizadas:
- **Linguagem de programação:** Python 3.12
- **Framework Web:** FastAPI
- **Banco de Dados:** MongoDB
- **ODM (Object Document Mapper):** Beanie
- **Gerenciador de Dependências:** uv

### Diagrama de classes
```mermaid
classDiagram
    direction LR
    class User {
        id: PydanticObjectId
        name: str
        email: EmailStr
        password: str
        creation_date: datetime
    }

    class Habit {
        id: PydanticObjectId
            name: str
        description: str | None
        active: bool
        started_date: datetime
        frequence: Frequence | None
        user: Link[User]

    }

    class Record {
        id: PydanticObjectId
        value: float
        status: Status
        comment: str | None
        creation_date: datetime
        habit: Link[Habit]
    }

    User --> "0..*" Habit : Link (Referência)
    Habit --> "0..*" Record : Link (Referência)
```

## Executando o projeto
1. Clone o repositório:
```bash
git clone https://github.com/rgcastrof/HabitTracker && cd HabitTracker
```
2. Crie e inicie o ambiente virtual:
```bash
uv venv --python 3.12 && source .venv/bin/activate
```

3. Instale as dependências:
```bash
uv sync
```

4. Inicie o servidor:
```bash
uvicorn --reload main:app
```

O servidor pode ser acessado em: http://127.0.0.1:8000
