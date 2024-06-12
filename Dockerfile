FROM python:3.8-slim

RUN pip install boto3 pymysql

COPY main.py /app/main.py

CMD ["python", "/app/main.py"]
