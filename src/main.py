import os
from dotenv import load_dotenv
import yaml
from bot import TelegramBotFramework

def main():
    # Load configuration from config.yml
    config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Get bot token from config.yml
    bot_token = config.get('bot')['default_bot_token']
    if not bot_token:
        raise ValueError("DEFAULT_BOT_TOKEN not found in config.yml")

    # Initialize and run the bot
    bot = TelegramBotFramework(bot_token)
    bot.run()

if __name__ == "__main__":
    main()