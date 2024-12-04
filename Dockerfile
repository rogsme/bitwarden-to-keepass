FROM python:3.11-slim-bookworm

WORKDIR /bitwarden-to-keepass

RUN apt-get update && \
    apt-get install -y --no-install-recommends wget unzip && \
    wget -O "bw.zip" "https://vault.bitwarden.com/download/?app=cli&platform=linux" && \
    unzip bw.zip && \
    chmod +x ./bw && \
    mv ./bw /usr/local/bin/bw && \
    apt-get purge -y --auto-remove wget unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf bw.zip

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-interaction --no-ansi

COPY . .

CMD ["./entrypoint.sh"]
