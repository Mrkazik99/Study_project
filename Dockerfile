FROM python:3.9-slim
EXPOSE 80
WORKDIR /app
RUN mkdir db
ADD requirements.txt .
RUN python3.9 -m pip install -r requirements.txt
ADD . ./
ENTRYPOINT [ "python", "main.py" ]