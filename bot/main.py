#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to handle '(my_)chat_member' updates.
Greets new users & keeps track of which chats the bot is in.

Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

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

# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets the user and records that they started a chat with the bot if it's a private chat.
    Since no `my_chat_member` update is issued when a user starts a private chat with the bot
    for the first time, we have to track it explicitly here.
    """
    user_name = update.effective_user.full_name


    logger.info("%s started a private chat with the bot", user_name)

    await update.effective_message.reply_text(
        f"Welcome {user_name}. Use /d to get word definition from Longman. Example: /d understand"
    )

async def get_definition(update: Update, context):
    word = context.args[0] if context.args else None

    if not word:
        await update.message.reply_text('Please provide a word. Example: /d hello')
        return

    # Replace this with your logic to get the definition of the word
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


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token('').build()



    # Interpret any other command or text message as a start of a private chat.
    # This will record the user as being in a private chat with bot.
    application.add_handler(CommandHandler('d', get_definition))

    application.add_handler(MessageHandler(filters.ALL, start_private_chat))

    # Run the bot until the user presses Ctrl-C
    # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
    # To reset this, simply pass `allowed_updates=[]`
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
    