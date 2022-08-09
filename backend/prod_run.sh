export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8001}

exec gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind $HOST:$PORT