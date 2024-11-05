import os
from dotenv import load_dotenv
import yaml
from bot import TelegramBotFramework

def main():
    # Load environment variables
    load_dotenv(override=True)
    
    # You may set bot token from superclass or let the baseclass get itself from environment 
    bot_token = os.getenv("DEFAULT_BOT_TOKEN", None) 
    
    bot = TelegramBotFramework(bot_token)
    bot.run()

if __name__ == "__main__":
    main()