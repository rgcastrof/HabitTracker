# HabitTracker
Sistema de Rastreamento de Hábitos

## Como usar
  - Clone o repositório
  ```bash
  https://github.com/rgcastrof/HabitTracker
  ```

  - Crie e entre no ambiente virtual
  ```bash
  python -m venv .venv && source .venv/bin/activate
  ```
  - Instale as dependências
  ```bash
  pip install -r requirements.txt
  ```
  - Executando o servidor
  ```bash
  uvicorn app.main:app --reload
  ```
  - Para gerar os 1000 dados fictícios
  ```bash
  python -m app.populate_db
  ```
## Acesse:

🌐 API Root: http://127.0.0.1:8000 📘 Swagger UI: http://127.0.0.1:8000/docs
