FROM ubuntu:20.04
FROM python:3.9

ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

CMD ["python3", "-m", "app"]