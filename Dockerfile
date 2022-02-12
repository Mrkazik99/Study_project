FROM python:3.9-slim
EXPOSE 20001
WORKDIR /app
RUN mkdir db
ADD requirements.txt .
RUN python3.9 -m pip install --no-cache-dir --upgrade -r requirements.txt
ADD main.py .
ADD db.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "20001"]
