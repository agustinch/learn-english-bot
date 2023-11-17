#!/usr/bin/python3
import pymongo
from pydantic import BaseModel
import pika, os, logging, time

logging.basicConfig()


class Goal(BaseModel):
    name: str
    date: str

def getSchedules():
    myclient = pymongo.MongoClient("mongodb://root:example@mongodb:27017")
    mydb = myclient["goals"]
    mycol = mydb["goals"]
    goals =  list(mycol.find({}, {"_id": 0}))
    print(goals)
    url = os.environ.get('CLOUDAMQP_URL','amqp://guest:guest@rabbitmq/%2f')
    params = pika.URLParameters(url)
    params.socket_timeout = 5

    connection = pika.BlockingConnection(params) # Connect to CloudAMQP
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='schedules') # Declare a queue

    for goal in goals:
        # Message to send to rabbitmq    
        channel.basic_publish(exchange='', routing_key='schedules', body=goal['name'])

    connection.close()

getSchedules()