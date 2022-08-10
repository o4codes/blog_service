export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8000}

exec uvicorn --reload --host $HOST --port $PORT "main:app"