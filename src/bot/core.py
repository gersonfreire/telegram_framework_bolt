#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

import yaml
from telegram import Update
from telegram.ext import Application, CommandHandler as TelegramCommandHandler, ContextTypes, PicklePersistence

from .handlers import CommandHandler
from .settings import Settings

# TODOs: 
# Embed persistence to the bot framework
# Embed the settings into the bot framework
# Add a method to change settings
# Add a command to display the settings
# Add a command to stop the bot
# embed the logging into the bot framework
# Add type hints to the class methods
# Add docstrings to the class methods


class TelegramBotFramework:
    def __init__(self, token: str = None, config_path: str = "config.yml"):
        
        # Get bot token from environment but overwrite it if it is provided inside .env file
        load_dotenv(override=True)
        env_token = os.getenv("DEFAULT_BOT_TOKEN")
        if not env_token:
            raise ValueError("DEFAULT_BOT_TOKEN not found in environment variables")
        
        self.token = token if token else env_token
        
        script_dir = Path(__file__).parent
        config_path = script_dir / config_path
        self.config_path = Path(config_path)
        self.settings = Settings()
        self.commands: Dict[str, CommandHandler] = {}
        self.logger = logging.getLogger(__name__)
        
        self._load_config()
        self._setup_logging()
        self._register_default_commands()

    def _load_config(self) -> None:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    def _setup_logging(self) -> None:
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

    def _register_default_commands(self) -> None:
        command_configs = self.config['bot']['commands']
        
        for cmd_name, cmd_config in command_configs.items():
            self.register_command(
                cmd_name,
                cmd_config['description'],
                cmd_config['response']
            )

    def register_command(self, name: str, description: str, response: str) -> None:
        self.commands[name] = CommandHandler(name, description, response)

    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        command = update.message.text.split()[0][1:]  # Remove the '/' prefix
        handler = self.commands.get(command)
        
        if handler:
            response = handler.get_response(self)
            await update.message.reply_text(response)

    async def handle_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        settings_str = self.settings.display()
        await update.message.reply_text(f"⚙️ Bot Settings:\n{settings_str}")

    async def post_init(self, app: Application) -> None:
        self.logger.info("Bot post-initialization complete!")
        admin_users = self.config['bot'].get('admin_users', [])
        for admin_id in admin_users:
            try:
                await app.bot.send_message(chat_id=admin_id, text="Bot post-initialization complete!")
            except Exception as e:
                self.logger.error(f"Failed to send message to admin {admin_id}: {e}")

    def run(self) -> None:
        app = Application.builder().token(self.token).build()

        async def get_bot_username():
            bot = await app.bot.get_me()
            return bot.username

        # bot_username = app.run(get_bot_username())
        bot_username = 'your_bot_name'
        persistence = PicklePersistence(filepath=f'{bot_username}_bot_data', update_interval=5)

        app = Application.builder().token(self.token).persistence(persistence).post_init(post_init=self.post_init).build()

        # Register command handlers
        for cmd_name in self.commands:
            app.add_handler(TelegramCommandHandler(cmd_name, self.handle_command))

        self.logger.info("Bot started successfully!")
        
        # Call post_init after initializing the bot
        app.run_polling()