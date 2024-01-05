#!/usr/bin/env python
import logging
from typing import Optional, Tuple
from scrapping import get_longman_definition
from telegram import Chat, ChatMember, ChatMemberUpdated, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import requests
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.full_name
    chat_id = update.effective_chat.id
    if chat_id in context.bot_data.get("user_ids", set()):
        await update.message.reply_text(f"{user_name}, please provide a word. Example: /d hello")
        return
    logger.info("%s started a private chat with the bot", user_name)
    context.bot_data.setdefault("user_ids", set()).add(chat_id)
    await update.effective_message.reply_text(
        f"Welcome {user_name}. Use /d to get word definition from Longman. Example: /d understand"
    )

async def get_definition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = context.args[0] if context.args else None

    if not word:
        await update.message.reply_text('Please provide a word. Example: /d hello')
        return

    definitions, audio = get_longman_definition(word)
    await update.message.reply_text(f'Definitions of *"{word}"*:', parse_mode=ParseMode.MARKDOWN)

    for sense_number, definition in definitions.items():
        await update.message.reply_text(f'*{sense_number}:* {definition}', parse_mode=ParseMode.MARKDOWN)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    if audio != '':
        audio_file = requests.get(audio, headers=headers)
        await update.message.reply_audio(audio=audio_file.content, title=f'Pronunciation of {word}')

    context.bot_data.setdefault("words", set()).add(context.bot_data.get("words", set()).add(word))


async def get_all_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words = [item for item in context.bot_data.get("words", set()) if item is not None]
    list_words = '\n'.join(words)
    if not words:
        await update.message.reply_text(f"You need to use /d to start")
        return
    await update.message.reply_text(f"You learnt these words:\n\n{list_words}")


    


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()

    
    application.add_handler(CommandHandler('d', get_definition))
    application.add_handler(CommandHandler('words', get_all_words))
    application.add_handler(MessageHandler(filters.ALL, start_private_chat))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
    