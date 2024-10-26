import logging
import os
from pathlib import Path
from typing import Dict, Optional

import yaml
from telegram import Update
from telegram.ext import Application, CommandHandler as TelegramCommandHandler, ContextTypes

from .handlers import CommandHandler
from .settings import Settings

class TelegramBotFramework:
    def __init__(self, token: str, config_path: str = "config.yml"):
        self.token = token
        script_dir = Path(__file__).parent
        config_path = script_dir / config_path
        self.config_path = Path(config_path)
        self.settings = Settings()
        self.commands: Dict[str, CommandHandler] = {}
        
        self._load_config()
        self._setup_logging()
        self._register_default_commands()

    def _load_config(self) -> None:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        # 'charmap' codec can't decode byte 0x8f in position 438: character maps to <undefined>
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

    def run(self) -> None:
        app = Application.builder().token(self.token).build()

        # Register command handlers
        for cmd_name in self.commands:
            app.add_handler(TelegramCommandHandler(cmd_name, self.handle_command))

        self.logger.info("Bot started successfully!")
        app.run_polling()