# setup

```
python -m .venv venv
source .venv/bin/activate
pip install -r requirements.txt

mv .env.example .env
```

# running

## development

```
flask init-db
flask run
```

## production

```
docker compose up --build -d
```
