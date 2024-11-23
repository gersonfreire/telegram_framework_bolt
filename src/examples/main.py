import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import yaml
from telegram import Update
from telegram.ext import Application, CommandHandler as TelegramCommandHandler, ContextTypes
from bot import TelegramBotFramework  # Import the TelegramBotFramework class

async def handle_echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echoes the user message back to the user

    Args:
        update (Update): The update object
        context (ContextTypes.DEFAULT_TYPE): The context object
    """
    
    user_message = update.message.text
    await update.message.reply_text(user_message)

def main():
    
    # Load environment variables
    # load_dotenv(override=True)
    
    # You may set bot token from superclass or let the baseclass itself get it from environment 
    # bot_token = os.getenv("DEFAULT_BOT_TOKEN", None) 
    
    bot = TelegramBotFramework()
    bot.run([handle_echo])

if __name__ == "__main__":
    main()