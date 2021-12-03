FROM python:3.9-slim
EXPOSE 80
WORKDIR /app
RUN mkdir db
ADD requirements.txt .
RUN python3.9 -m pip install --no-cache-dir --upgrade -r requirements.txt
ADD . ./
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
