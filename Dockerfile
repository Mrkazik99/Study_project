FROM python:3.9-slim
WORKDIR /app
ENTRYPOINT [ "python", "main.py" ]