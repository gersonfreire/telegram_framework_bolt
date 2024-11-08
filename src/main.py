import os
from dotenv import load_dotenv
import yaml
from telegram import Update
from telegram.ext import Application, CommandHandler as TelegramCommandHandler, ContextTypes
from bot import TelegramBotFramework

async def handle_echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    await update.message.reply_text(user_message)

def main():
    # Load environment variables
    load_dotenv(override=True)
    
    # You may set bot token from superclass or let the baseclass get itself from environment 
    bot_token = os.getenv("DEFAULT_BOT_TOKEN", None) 
    
    bot = TelegramBotFramework(bot_token)
    bot.run([handle_echo])

if __name__ == "__main__":
    main()