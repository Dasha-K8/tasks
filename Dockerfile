
FROM python:3.13

WORKDIR /task_copy

COPY practice.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "practice.py"]




