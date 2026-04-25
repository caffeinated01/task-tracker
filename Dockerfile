FROM python:3.14-slim

WORKDIR /app

ENV PYTHONUNBUFFERED="true" PYTHONDONTWRITEBYTECODE="true"

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app/ ./app/
COPY entrypoint.sh .
RUN mkdir -p /app/instance

RUN chmod +x entrypoint.sh

RUN useradd -m -u 1000 appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:app"]