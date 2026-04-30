FROM python:3.14-slim

WORKDIR /app

ARG FLASK_PORT=8000
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

EXPOSE ${FLASK_PORT}

ENTRYPOINT ["/app/entrypoint.sh"]


# https://github.com/privacyidea/privacyidea/issues/4067
# in nginx proxy manager, set the following rules under 'custom location' `/api/`
# proxy_set_header X-Forwarded-Proto https;
# proxy_set_header X-Forwarded-Scheme https;
# to prevent 'Mixed-Content' error when hitting api endpts from frontend
CMD ["sh", "-c", "gunicorn --worker-class=gthread --workers=${GUNICORN_WORKERS} --threads=${GUNICORN_THREADS} --forwarded-allow-ips=* --bind=0.0.0.0:${FLASK_PORT} app.wsgi:app"]