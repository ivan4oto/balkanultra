#!/bin/sh

# Wait for the database to be ready
# while ! nc -z db 5432; do
#   echo "Waiting for the database..."
#   sleep 1
# done

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Start the Django app
echo "Starting Django app..."
exec "$@"
