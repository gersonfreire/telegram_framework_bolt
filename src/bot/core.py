#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.1.0"

import asyncio
import logging
import os
from pathlib import Path
import sys
from typing import Dict, Optional
from dotenv import load_dotenv

import yaml
from telegram import Update
from telegram.ext import Application, CommandHandler as TelegramCommandHandler, ContextTypes, PicklePersistence
from telegram.constants import ParseMode

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

from pathlib import Path
import os
import sys

def get_main_script_path() -> Path:
    return (Path(os.path.abspath(sys.modules['__main__'].__file__)))

def get_config_path(config_filename: str = "config.yml") -> Path:
    config_path = get_main_script_path()
    return config_path.parent / config_filename

class TelegramBotFramework:
    
    def __init__(self, token: str = None, config_filename: str = get_config_path(), env_file: Path = None):        
        
        self.logger = logging.getLogger(__name__)
        
        # Get the path of the main executed script
        main_script_path = get_main_script_path()
        self.logger.debug(f"The main script folder path is: {main_script_path}")                
        
        # Get bot token from environment but overwrite it if it is provided inside .env file
        self.env_file = main_script_path.parent / ".env" or env_file
        load_dotenv(override=True, dotenv_path=str(self.env_file))
        env_token = os.getenv("DEFAULT_BOT_TOKEN")
        if not env_token:
            raise ValueError("DEFAULT_BOT_TOKEN not found in environment variables")
        
        self.token = token if token else env_token
        
        self.config_path = config_filename
        self.settings = Settings()
        self.commands: Dict[str, CommandHandler] = {}
        
        self.app: Optional[Application] = None
        self.registered_handlers = {}
        
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
        """Generic handler for bot commands

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        
        try:
            command = update.message.text.split()[0][1:]  # Remove the '/' prefix
            handler = self.commands.get(command)
            
            if handler:
                response = await handler.get_response(self)
                await update.message.reply_text(response)
        except Exception as e:
            self.logger.error(f"Error handling command: {e}")
            await update.message.reply_text("An error occurred while handling the command.")

    async def handle_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Configure bot settings

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        
        settings_str = self.settings.display()
        await update.message.reply_text(f"⚙️ Bot Settings:\n{settings_str}")

    async def handle_list_commands(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """List available commands

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        
        try:
            logging.info("Listing available commands")
            commands_list = "\n".join(
                f"/{cmd} - {handler.description}"
                for cmd, handler in self.commands.items()
            )
            await update.message.reply_text(f"Available commands:\n{commands_list}")
        except Exception as e:
            self.logger.error(f"Error listing commands: {e}")
            await update.message.reply_text("An error occurred while listing commands.")

    async def post_init(self, app: Application) -> None:
        self.logger.info("Bot post-initialization complete!")
        admin_users = self.config['bot'].get('admin_users', [])
        for admin_id in admin_users:
            try:
                await app.bot.send_message(chat_id=admin_id, text="Bot post-initialization complete!")
            except Exception as e:
                self.logger.error(f"Failed to send message to admin {admin_id}: {e}")

        # Set bot commands dynamically
        bot_commands = [
            (f"/{cmd}", handler.description)
            for cmd, handler in self.commands.items()
        ]
        # my_commands = await app.bot.get_my_commands()
        await app.bot.set_my_commands(bot_commands)        
            
        my_commands = await app.bot.get_my_commands()
        commands_dict = {
            cmd.command: cmd.description or app.bot.commands[cmd.command].__doc__
            for cmd in my_commands
        }
        
        registered_handlers = [handler.callback.__name__ for handler in app.handlers[0]]
        
        registered_handlers = [
            f"{handler.callback.__name__}: {', '.join(handler.commands)}"
            for handler in app.handlers[0] if hasattr(handler, 'commands')
        ]
        
        for handler in app.handlers[0]:
            if hasattr(handler, 'commands'):
                    docstring = handler.callback.__doc__.split('\n')[0] if handler.callback.__doc__ else "No docstring available"
                    self.registered_handlers[', '.join(handler.commands)] = {
                        'handler': handler.callback.__name__,
                        'command': ', '.join(handler.commands),
                        'docstring': docstring
                    }
        
        self.logger.info(f"Registered handlers: {registered_handlers}")    

    def run(self, external_handlers:list) -> None:
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

        # Register the list_commands handler
        app.add_handler(TelegramCommandHandler("list_commands", self.handle_list_commands))

        # Register the external handlers
        for handler in external_handlers:
            app.add_handler(TelegramCommandHandler("echo", handler))

        self.logger.info("Bot started successfully!")
        
        self.app = app
        
        # Call post_init after initializing the bot
        app.run_polling()