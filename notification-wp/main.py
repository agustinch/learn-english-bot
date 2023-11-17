import pymongo
from pydantic import BaseModel
import pika, os, logging, time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


logging.basicConfig()


class Goal(BaseModel):
    name: str
    date: str


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hola wuacho")
    print(update.message.chat_id)

if __name__ == '__main__':
    application = ApplicationBuilder().token('').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()

def getSchedules():
    
    url = os.environ.get('CLOUDAMQP_URL','amqp://guest:guest@localhost/%2f')
    params = pika.URLParameters(url)
    params.socket_timeout = 5

    connection = pika.BlockingConnection(params) # Connect to CloudAMQP
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='schedules') # Declare a queue
    
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    
    connection.close()

getSchedules()