FROM python:3.11-slim

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 仮想環境を作る必要性がないので作成しない
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN pip install poetry
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "fast_todo.app:app"]
