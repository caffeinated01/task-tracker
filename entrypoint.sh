#!/bin/bash
set -e
 
if [ ! -f /app/instance/app.db ]; then
    echo "Database not found, initialising..."
    flask init-db
else
    echo "Database already exists, skipping initialisation."
fi
 
exec "$@"
 