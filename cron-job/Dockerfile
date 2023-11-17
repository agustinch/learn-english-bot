FROM python:3.8

RUN apt-get update && apt-get -y install cron vim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py ./main.py
# Add cron job to run every day at 3:30 PM
RUN echo "*/1 * * * * cd /app && /usr/bin/env /usr/bin/python3 main.py >> cron_log.log 2>&1" > /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab
RUN echo $PYTHONPATH
RUN service cron start
CMD ["cron", "-f"]