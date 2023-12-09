#!/bin/sh

until cd /app/news_project
do
    echo "Waiting for server volume..."
done

celery -A config.celery worker --loglevel=info --concurrency 1 -E
