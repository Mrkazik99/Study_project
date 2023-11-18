FROM python:3.11-slim
EXPOSE 20001
WORKDIR /app
ADD . ./
RUN python3.11 -m pip install .
CMD ["uvicorn", "service_management_system.main:app", "--host", "0.0.0.0", "--port", "20001"]
