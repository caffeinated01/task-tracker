FROM python:3.14-slim

WORKDIR /app

ENV PYTHONUNBUFFERED="true"
ENV PYTHONDONTWRITEBYTECODE="true"

RUN apt-get update 
RUN apt-get install -y

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app/ ./app/
COPY entrypoint.sh .
COPY .env .

RUN useradd -m -u 1000 appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:app"]