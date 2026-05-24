FROM python:3.14-slim-bookworm

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN uv pip install --system -r requirements.txt 

COPY serve.py .

ENV MLFLOW_TRACKING_URI=http://192.168.1.171:5000

EXPOSE 8000


CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]

