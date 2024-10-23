import os
from dotenv import load_dotenv
from bot import TelegramBotFramework

def main():
    # Load environment variables
    load_dotenv()
    
    # Get bot token from environment
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN not found in environment variables")

    # Initialize and run the bot
    bot = TelegramBotFramework(bot_token)
    bot.run()

if __name__ == "__main__":
    main()