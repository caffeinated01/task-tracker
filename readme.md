# setup

```
python -m .venv venv
source .venv/bin/activate
pip install -r requirements.txt
```

# running

```
flask init-db
flask run
```

use gunicorn for production:

```
gunicorn app.wsgi:app
```
