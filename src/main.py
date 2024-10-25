import os
from dotenv import load_dotenv
from bot import TelegramBotFramework

def main():
    # Load environment variables
    load_dotenv()
    
    # Get bot token from environment but overwrite it if it is provided inside .env file
    load_dotenv(override=True)
    bot_token = os.getenv("DEFAULT_BOT_TOKEN")
    if not bot_token:
        raise ValueError("DEFAULT_BOT_TOKEN not found in environment variables")

    # Initialize and run the bot
    bot = TelegramBotFramework(bot_token)
    bot.run()

if __name__ == "__main__":
    main()