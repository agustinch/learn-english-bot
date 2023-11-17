import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, Updater

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hola wuacho")
    await context.bot.send_message(chat_id='6583338363', text=update.message.chat_id)

async def message(application):
     await application.updater.bot.send_message(chat_id='6583338363', text='Holaa', )


if __name__ == '__main__':
    application = ApplicationBuilder().token('6472333311:AAHeqNLiy53cUnyDSYMA2oMw_9kzx7iUy6E').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    asyncio.run(message(application))
    application.run_polling()
