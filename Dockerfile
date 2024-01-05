FROM python:3.8

RUN apt-get update && apt-get -y install cron vim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py ./main.py


CMD ["python", "main.py"]