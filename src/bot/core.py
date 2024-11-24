#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.4.57 chore: Update version to 0.4.55 and refactor version string"

"""TODO's:
full command line on show version and post init only for admins
Change interval status
Clear and update telegram command menu from handlers
get external ip address on version command instead of internal local ip address
"""

import asyncio
import datetime
from functools import wraps
import json
import logging
import os
from pathlib import Path
import sys
from typing import Dict, Optional, List
from dotenv import load_dotenv
import dotenv
import socket
import requests

import yaml
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler as TelegramCommandHandler, ContextTypes, PicklePersistence, CallbackContext, filters, JobQueue
from telegram.constants import ParseMode

from .handlers import CommandHandler
from .settings import Settings
from .util_functions import call_function, call_and_convert_function, call_function_with_converted_args, convert_params, convert_values_to_types, get_function_argument_types

from pathlib import Path
import os
import sys

# import bot.util_decorators as util_decorators

logger = logging.getLogger(__name__)
def get_main_script_path() -> Path: 
    return (Path(os.path.abspath(sys.modules['__main__'].__file__)))

def get_config_path(config_filename: str = "config.yml") -> Path:
    config_path = get_main_script_path()
    return config_path.parent / config_filename

class TelegramBotFramework:

    async def send_message_to_admins(self, context: CallbackContext, message: str) -> None:
        """Send a message to all admin users.

        Args:
            context (CallbackContext): The context object
            message (str): The message to send
        """
        for chat_id in self.admin_users:
            try:
                await context.bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                self.logger.error(f"Failed to send message to admin {chat_id}: {e}")
        return    
        
    async def setup_new_user(self,  update: Update, context: CallbackContext) -> None:
        
        try:
            user_id = update.effective_user.id
            
            new_user_data = {
                'user_id': user_id,
                'username': update.effective_user.username,
                'first_name': update.effective_user.first_name,
                'last_name': update.effective_user.last_name,
                'language_code': update.effective_user.language_code,
                'last_message': update.message.text if not update.message.text.startswith('/') else None,
                'last_command': update.message.text if update.message.text.startswith('/') else None,
                'last_message_date': update.message.date if not update.message.text.startswith('/') else None,
                'last_command_date': update.message.date if update.message.text.startswith('/') else None
            }
            
            for key, value in new_user_data.items():
                try:
                    context.user_data[key] = value
                    await context.application.persistence.update_user_data(user_id, data={key: value})
                except Exception as e:
                    self.logger.error(f"Error updating user data: {e}")
            
            # flush all users data to persistence
            await context.application.persistence.flush()
            
            # check user data
            user_data = await context.application.persistence.get_user_data()
            self.logger.debug(f"User data: {user_data}")

        except Exception as e:
            self.logger.error(f"Error setting up new user: {e}")
    
    async def send_status_message(self, context: CallbackContext) -> None:
        try:
            if self._load_status_message_enabled():
                for chat_id in self.admin_users:
                    try:
                        await context.bot.send_message(chat_id=chat_id, text="The bot is still active.")
                    except Exception as e:
                        self.logger.error(f"Failed to send status message to admin {chat_id}: {e}")

            # Check for the "sched_command" item in persistent bot data
            sched_command = self.app.bot_data.get("sched_command")
            
            # TODO: if type of sched_command is list then execute each item
            if sched_command.startswith("[") and sched_command.endswith("]"):
                sched_command = list(json.loads(sched_command))
                for value in sched_command:
                    try:
                        parts = value.split()
                        if len(parts) < 2:
                            error_message = f"Invalid sched_command format for {value}. Expected at least module name and function name."
                            self.logger.error(error_message)
                            await self.send_message_to_admins(context, f"Error: {error_message}")
                            continue

                        module_name = parts[0]
                        function_name = parts[1]
                        function_params = " ".join(parts[2:])

                        # result = call_function(module_name, function_name, function_params)
                        result = call_function_with_converted_args(module_name, function_name, function_params)
                        
                        self.logger.info(f"Executed sched_command for {value} with result: {result}")
                        await self.send_message_to_admins(context, f"Result of {value}:\n{result}")
                        
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        self.logger.error(f"Error executing sched_command for {value} in {fname} at line {exc_tb.tb_lineno}: {e}")
            
            else:
            # if there is a sched_command, execute it
            # if sched_command:
                try:
                    # Split the command into module name, function name, and parameters
                    parts = sched_command.split()
                    if len(parts) < 2:
                        error_message = "Invalid sched_command format. Expected at least module name and function name."
                        self.logger.error(error_message)
                        # Call the function to send the error message to all administrators
                        await self.send_message_to_admins(context, f"Error: {error_message}")

                    module_name = parts[0]
                    function_name = parts[1]
                    function_params = " ".join(parts[2:])

                    # Call the function using the call_function utility
                    result = call_function(module_name, function_name, function_params)
                    self.logger.info(f"Executed sched_command: {sched_command} with result: {result}")
                    
                    # send the result for each administrator user
                    await self.send_message_to_admins(context, f"Result of {sched_command}:\n{result}")
                    
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    self.logger.error(f"Error executing sched_command in {fname} at line {exc_tb.tb_lineno}: {e}")
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logger.error(f"Error in send_status_message in {fname} at line {exc_tb.tb_lineno}: {e}")
     
    def with_typing_action(handler):
        @wraps(handler)
        async def wrapper(self, update: Update, context: CallbackContext, *args, **kwargs):
            try:
                logger.debug("Sending typing action")
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
                return await handler(self, update, context, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error: {e}")
                return await handler(self, update, context, *args, **kwargs)
        return wrapper

    def with_log_admin(handler):
        @wraps(handler)
        async def wrapper(self, update: Update, context: CallbackContext, *args, **kwargs):
            
            try:
                user_id = update.effective_user.id
                user_name = update.effective_user.full_name
                command = update.message.text
                
                if int(user_id) not in self.admin_users:                    
                    for admin_user_id in self.admin_users:
                        try:
                                log_message = f"Command: {command}\nUser ID: {user_id}\nUser Name: {user_name}"
                                logger.debug(f"Sending log message to admin: {log_message}")                            
                                await context.bot.send_message(chat_id=admin_user_id, text=log_message, parse_mode=ParseMode.MARKDOWN)
                        except Exception as e:
                            logger.error(f"Failed to send log message to admin {admin_user_id}: {e}")

                return await handler(self, update, context, *args, **kwargs)
                
            except Exception as e:
                logger.error(f"Error: {e}")
                return await handler(self, update, context, *args, **kwargs)
        return wrapper

    def with_register_user(handler):
        @wraps(handler)
        async def wrapper(self, update: Update, context: CallbackContext, *args, **kwargs):
            
            try:                
                await self.setup_new_user(update, context)

                return await handler(self, update, context, *args, **kwargs)
            
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                error_message = f"Error getting user data in {fname} at line {exc_tb.tb_lineno}: {e}"
                self.logger.error(error_message)               
                await update.message.reply_text(error_message, parse_mode=None)
            
        return wrapper
    
    def __init__(self, token: str = None, admin_users: List[int] = [], config_filename: str = get_config_path(), env_file: Path = None):     
        
        self.version = __version__   
        
        self.logger = logging.getLogger(__name__)
        
        # Get the path of the main executed script
        main_script_path = get_main_script_path()
        self.logger.debug(f"The main script folder path is: {main_script_path}")                
        
        # Get bot token from environment but overwrite it if it is provided inside .env file
        # main_script_path = Path(get_main_script_path() or os.path.abspath(__file__))
        self.env_file = main_script_path.parent / ".env" or env_file
        load_dotenv(override=True, dotenv_path=str(self.env_file))
        env_token = os.getenv("DEFAULT_BOT_TOKEN")
        if not env_token:
            raise ValueError("DEFAULT_BOT_TOKEN not found in environment variables")
        
        self.token = token if token else env_token
        self.admin_users = list(map(int, dotenv.get_key(dotenv.find_dotenv(), "ADMIN_ID_LIST").split(','))) or admin_users
        
        self.config_path = config_filename
        self.settings = Settings()
        self.commands: Dict[str, CommandHandler] = {}
        
        self.app: Optional[Application] = None
        self.registered_handlers = {}
        
        self._load_config()
        self._setup_logging()
        self._register_default_commands()
        
        # Default value for send_status_interval
        self.send_status_interval = 60  # Default value (1 minute)

    def _load_status_message_enabled(self) -> bool:
        """Load the status_message_enabled value from persistent data."""
        if 'status_message_enabled' in self.app.bot_data:
            return self.app.bot_data['status_message_enabled']
        return True  # Default value

    def _save_status_message_enabled(self) -> None:
        """Save the status_message_enabled value to persistent data."""
        self.app.bot_data['status_message_enabled'] = self.status_message_enabled

    def _load_send_status_interval(self) -> int:
        """Load the send_status_interval value from persistent data."""
        if 'send_status_interval' in self.app.bot_data:
            return self.app.bot_data['send_status_interval']
        return 60  # Default value

    def _save_send_status_interval(self) -> None:
        """Save the send_status_interval value to persistent data."""
        self.app.bot_data['send_status_interval'] = self.send_status_interval

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

    @with_typing_action
    @with_log_admin
    @with_register_user
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
                # TODO: pass the user to filter the help command
                response = await handler.get_response(self, update, context)
                await update.message.reply_text(response)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error_message = f"Error getting user data in {fname} at line {exc_tb.tb_lineno}: {e}"
            self.logger.error(error_message)               
            await update.message.reply_text(error_message, parse_mode=None)

    @with_typing_action
    @with_log_admin
    @with_register_user
    async def handle_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Configure bot settings

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        
        settings_str = self.settings.display()
        await update.message.reply_text(f"⚙️ Bot Settings:\n{settings_str}")

    @with_typing_action
    @with_log_admin
    @with_register_user
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

    @with_typing_action 
    @with_log_admin
    @with_register_user
    async def cmd_git(self, update: Update, context: CallbackContext):
        """Update the bot's version from a git repository"""
        
        try:
            # get the branch name from the message
            # branch_name = update.message.text.split(' ')[1]
            message = f"_Updating the bot's code from the branch..._" # `{branch_name}`"
            self.logger.info(message)
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            
            # update the bot's code
            # command = f"git fetch origin {branch_name} && git reset --hard origin/{branch_name}"
            command = "git status"
            
            if len(update.effective_message.text.split(' ')) > 1:
                git_command = update.effective_message.text.split(' ')[1]
                self.logger.info(f"git command: {command}")
                command = f"git {git_command}"
            
            # execute system command and return the result
            # os.system(command=command)
            result = os.popen(command).read()
            self.logger.info(f"Result: {result}")
            
            result = f"_Result:_ `{result}`"
            
            await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            self.logger.error(f"Error: {e}")
            await update.message.reply_text(f"An error occurred: {e}")

    # @with_typing_action
    # @with_log_admin
    # @with_register_user
    async def restart_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Command to restart the bot

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        
        try:
            await update.message.reply_text("_Restarting..._", parse_mode=ParseMode.MARKDOWN)
            args = sys.argv[:]
            args.insert(0, sys.executable)
            os.chdir(os.getcwd())
            os.execv(sys.executable, args)
            
        except Exception as e:
            self.logger.error(f"Error restarting bot: {e}")
            await update.message.reply_text(f"An error occurred while restarting the bot: {e}")

    # @with_typing_action 
    # @with_log_admin
    # @with_register_user
    async def stop_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Command to stop the bot

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        
        try:            
            await context.application.persistence.flush()
            
            # check user data
            user_data = await context.application.persistence.get_user_data()
            self.logger.debug(f"User data: {user_data}")
            
            await update.message.reply_text(f"*{update._bot.username} STOPPED!*", parse_mode=ParseMode.MARKDOWN)
            await context.job_queue.stop()
            await context.application.stop()
            # await context.application.shutdown()

            args = sys.argv[:]
            args.insert(0, 'stop')
            args = None
            os.chdir(os.getcwd())
            os.abort()
            
        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}")
            await update.message.reply_text(f"An error occurred while stopping the bot: {e}")

    async def cmd_stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            await update.message.reply_text(f"*{update._bot.username} STOPPED!*", parse_mode=ParseMode.MARKDOWN)
            
            if not self.app.running:
                raise RuntimeError("This Application is not running!")

            self.app._running = False
            self.logger.info("Application is stopping. This might take a moment.")

            await context.job_queue.stop(wait=False)
            
            _STOP_SIGNAL = object()
            await self.app.update_queue.put(_STOP_SIGNAL)
            self.logger.debug("Waiting for update_queue to join")
            
            self.logger.debug("Application stopped fetching of updates.")

            if self.app._job_queue:
                self.logger.debug("Waiting for running jobs to finish")
            await self.app._job_queue.stop(wait=True)  # type: ignore[union-attr]
            self.logger.debug("JobQueue stopped")

            self.logger.debug("Waiting for `create_task` calls to be processed")

            self.logger.info("Application.stop() complete")
            
            os.chdir(os.getcwd())
            os.abort()
        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}")
            await update.message.reply_text(f"An error occurred while stopping the bot: {e}")

    @with_typing_action
    @with_log_admin
    @with_register_user
    async def show_user_data(self, update: Update, context: CallbackContext):
        """Show current persistent user data"""
        
        try:
            # Fix 'Object of type datetime is not JSON serializable' error
            def default_converter(o):
                if isinstance(o, datetime.datetime):
                    return o.isoformat()
                raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

            json_data = json.dumps(context.user_data, indent=4, default=default_converter)
            formatted_json = f"```json\n{json_data}\n```"
            await update.message.reply_text(f"_User persistent data:_ {os.linesep}{formatted_json}", parse_mode=ParseMode.MARKDOWN)
            formatted_json = f"`{json_data}`"           
            
        except Exception as e:
            self.logger.error(f"Error showing user data: {e}")
            await update.message.reply_text("An error occurred while showing user data.")

    @with_typing_action
    @with_log_admin
    @with_register_user
    async def cmd_get_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """List all registered users  

        Args:
            update (Update): The update object
            context (ContextTypes.DEFAULT_TYPE): The context object
        """
        try:
            users_data = await context.application.persistence.get_user_data()
            users_list = "\n".join(
                f"User ID: {user_id}, Username: {user_data.get('username', 'N/A')}, First Name: {user_data.get('first_name', 'N/A')}, Last Name: {user_data.get('last_name', 'N/A')}"
                for user_id, user_data in users_data.items()
            )
            await update.message.reply_text(f"Registered Users:\n{users_list}")
        except Exception as e:
            self.logger.error(f"Error listing registered users: {e}")
            await update.message.reply_text("An error occurred while listing registered users.")
      
    @with_typing_action
    @with_log_admin
    @with_register_user
    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /start command

        Args:
            update (Update): The update object
            context (ContextTypes.DEFAULT_TYPE): The context object
        """
        try:
            user_id = update.effective_user.id
            bot_username = (await context.bot.get_me()).username
            start_message = (
                f"👋 Welcome! I'm here to help you. Use /help to see available commands.\n\n"
                f"TelegramBotFramework version: {__version__}\n"
                f"Your Telegram ID: {user_id}\n"
                f"Bot Username: @{bot_username}"
            )
            await update.message.reply_text(start_message)
        except Exception as e:
            self.logger.error(f"Error handling /start command: {e}")
            await update.message.reply_text("An error occurred while handling the /start command.")
            
    @with_typing_action
    @with_log_admin
    @with_register_user
    async def handle_version(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /version command

        Args:
            update (Update): The update object
            context (ContextTypes.DEFAULT_TYPE): The context object
        """
        try:
            user_id = update.effective_user.id
            bot_username = (await context.bot.get_me()).username
            version_message = (
                f"TelegramBotFramework version: {__version__}\n"
                f"Your Telegram ID: {user_id}\n"
                f"Bot Username: @{bot_username}"
            )
            
            if user_id in self.admin_users:
                main_script_path = get_main_script_path()
                command_line = " ".join(sys.argv)
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                try:
                    external_ip = requests.get('https://api.ipify.org', timeout=5).text
                except requests.RequestException as e:
                    external_ip = ip_address
                version_message += (
                    f"\nMain Script Path: {main_script_path}"
                    f"\nCommand Line: {command_line}"
                    f"\nHostname: {hostname}"
                    f"\nServer IP Address: {external_ip}"
                )
            
            await update.message.reply_text(version_message)
        except Exception as e:
            self.logger.error(f"Error handling /version command: {e}")
            await update.message.reply_text("An error occurred while handling the /version command.")

    @with_typing_action
    @with_log_admin
    @with_register_user
    async def update_library(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /update_library command to update the tlgbotfwk library

        Args:
            update (Update): The update object
            context (ContextTypes.DEFAULT_TYPE): The context object
        """
        try:
            await update.message.reply_text("Updating the tlgbotfwk library...")

            # Execute the pip install command
            result = os.popen("pip install --upgrade tlgbotfwk").read()

            await update.message.reply_text(f"Update result:\n{result}")
        except Exception as e:
            self.logger.error(f"Error updating tlgbotfwk library: {e}")
            await update.message.reply_text("An error occurred while updating the tlgbotfwk library.")
   
    @with_typing_action
    @with_log_admin
    @with_register_user
    async def toggle_status_message(self, update: Update, context: CallbackContext) -> None:
        """Toggle the status message on or off to indicate whether the bot is active.

        Args:
            update (Update): _description_
            context (CallbackContext): _description_
        """
        user_id = update.effective_user.id
        if user_id in self.admin_users:
            self.status_message_enabled = not self.status_message_enabled
            self._save_status_message_enabled()
            status = "enabled" if self.status_message_enabled else "disabled"
            await update.message.reply_text(f"Status message has been {status}.")
        else:
            await update.message.reply_text("You are not authorized to use this command.")
          
    @with_typing_action
    @with_log_admin
    @with_register_user
    async def change_status_interval(self, update: Update, context: CallbackContext) -> None:
        """Change the interval for sending status messages and restart the job

        Args:
            update (Update): The update object
            context (CallbackContext): The context object
        """
        try:
            user_id = update.effective_user.id
            if user_id not in self.admin_users:
                await update.message.reply_text("You are not authorized to use this command.")
                return
            
            # Get the new interval from the command arguments
            args = context.args
            if not args or not args[0].isdigit():
                await update.message.reply_text("Please provide a valid interval in minutes.")
                return
            
            self.send_status_interval = int(args[0]) * 60 # Convert minutes to seconds
            self._save_send_status_interval()
            
            # Stop and delete all running jobs
            current_jobs = context.job_queue.jobs()
            for job in current_jobs:
                job.schedule_removal()
            
            # Restart the job with the new interval
            job_queue: JobQueue = self.app.job_queue
            self.job_queue = context.job_queue.run_repeating(self.send_status_message, interval=self.send_status_interval, first=0)            
            
            await update.message.reply_text(f"Status message interval has been changed to {args[0]} minutes.")
        except Exception as e:
            self.logger.error(f"Error changing status interval: {e}")
            await update.message.reply_text("An error occurred while changing the status interval.")
            
    @with_typing_action
    @with_log_admin
    @with_register_user
    async def call_function_command(self, update: Update, context: CallbackContext) -> None:
        """Admin-only command to call a function dynamically

        Args:
            update (Update): The update object
            context (CallbackContext): The context object
        """
        try:
            user_id = update.effective_user.id
            if user_id not in self.admin_users:
                await update.message.reply_text("You are not authorized to use this command.")
                return
            
            # Get the module name, function name, and function parameters from the command arguments
            args = context.args
            if len(args) < 2:
                await update.message.reply_text("_Please provide at least the module name and function name, and optionally function parameters._", parse_mode=ParseMode.MARKDOWN)
                
                # show a real working example
                await update.message.reply_text("_Example usage:_\n`/call_function math pow 2,3`", parse_mode=ParseMode.MARKDOWN)
                await update.message.reply_text("_Example usage:_\n`/call_function bot.util_functions hello_world_noparam`", parse_mode=ParseMode.MARKDOWN)                             
                
                return
            
            module_name = args[0]
            function_name = args[1]            
            result = call_function_with_converted_args(module_name, function_name, " ".join(args[2:]))
            logger.debug(result)             
            
            json_data = json.dumps(result, indent=4)
                        
            formatted_json = f"```json\n{json_data}\n```"
            await update.message.reply_text(f"_Result:_ {os.linesep}{formatted_json}", parse_mode=ParseMode.MARKDOWN)
                        
        except Exception as e:
            self.logger.error(f"Error calling function: {e}")
            await update.message.reply_text("An error occurred while calling the function.")
    
    @with_typing_action
    @with_log_admin
    @with_register_user
    async def show_bot_data(self, update: Update, context: CallbackContext) -> None:
        """Show current bot data in JSON format"""
        try:
            bot_data = {
                "version": self.version,
                "admin_users": self.admin_users,
                "config_path": str(self.config_path),
                "settings": self.settings.display(),
                "commands": list(self.commands.keys()),
                "status_message_enabled": self.status_message_enabled,
                "send_status_interval": self.send_status_interval,
            }
            bot_data = context.bot_data # await context.application.persistence.get_bot_data()
            bot_data_json = json.dumps(bot_data, indent=4)
                        
            formatted_json = f"```json\n{bot_data_json}\n```"
            await update.message.reply_text(f"_Bot persistent data:_ {os.linesep}{formatted_json}", parse_mode=ParseMode.MARKDOWN)
                        
        except Exception as e:
            self.logger.error(f"Error showing bot data: {e}")
            await update.message.reply_text("An error occurred while showing bot data.")    
    
    @with_typing_action
    @with_log_admin
    @with_register_user
    async def eval_exec_command(self, update: Update, context: CallbackContext) -> None:
        """Admin-only command to evaluate a Python expression.

        Args:
            update (Update): The update object
            context (CallbackContext): The context object
        """
        try:
            command = update.message.text.split()[0][1:]  # Remove the '/' prefix
            command_type = "exec" if command == "exec" else "eval"
            
            user_id = update.effective_user.id
            if user_id not in self.admin_users:
                await update.message.reply_text("You are not authorized to use this command.")
                return

            # Get the expression from the command arguments
            expression = " ".join(context.args)
            if not expression:
                await update.message.reply_text('please provide an expression to evaluate.\nExample:\n/exec x = 10\nif x > 5:\n\tresult = "x is greater than 5"\nelse:\n\tresult = "x is not greater than 5"', parse_mode=ParseMode.MARKDOWN)
                return

            # Evaluate the expression according to the command type
            if command_type == "exec":
                # code = '/exec x = 10\nif x > 5:\n\tresult = "x is greater than 5"\nelse:\n\tresult = "x is not greater than 5"'   
                code = update.message.text[len(command) + 2:]
                
                # replace special tab and line break characters
                code = code.replace("\\n", "\n").replace("\\t", "\t")
                
                local_vars = {}
                exec(code, {}, local_vars)
                result = local_vars
                # Access the result of the conditional statement
                # result = local_vars['result']
                self.logger.debug(result)  # Output: x is greater than 5                
            else:
                result = eval(expression)
            
            result = json.dumps(result, indent=4)

            # Send the result back to the user
            # await update.message.reply_text(f"Result: {result}")
            await update.message.reply_text(f"```json\n{result}\n```", parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            self.logger.error(f"Error evaluating expression: {e}")
            await update.message.reply_text(f"{e}")
            await update.message.reply_text('please provide an expression to evaluate.\nExample:\n/exec x = 10\nif x > 5:\n\tresult = "x is greater than 5"\nelse:\n\tresult = "x is not greater than 5"', parse_mode=ParseMode.MARKDOWN)
    
    @with_typing_action
    @with_log_admin
    @with_register_user
    async def set_bot_data(self, update: Update, context: CallbackContext) -> None:
        """Command to set bot data

        Args:
            update (Update): The update object
            context (CallbackContext): The context object
        """
        try:
            args = context.args
            if len(args) < 2:
                await update.message.reply_text("Please provide both the key and value.\nUsage: /set_bot_data <key> <value>")
                return

            key = args[0]
            
            # if args[1] begins with double quotes try to join the rest of arguments in one
            if args[1].strip().startswith('"'):
                value = " ".join(args[1:])
                args[1] = value
                
                # remove args greater than 1
                args = args[:2]
                
                if value.endswith('"'):
                    value = value[1:-1]
            else:
                # TODO: handle the case when value is a list or a dictionary '{math pow 2,3}'
                if args[1].strip().startswith('[') and args[-1].strip().endswith(']'):
                    try:
                        value = " ".join(args[1:])
                        
                        # remove args greater than 1
                        args[1] = value
                        args = args[:2]      
                                          
                    except json.JSONDecodeError as e:
                        await update.message.reply_text(f"Error parsing object list or dictionary: {e}")
                        return
                
                value = args[1]
            
            # convert type of value according third parameter
            if len(args) > 2:
                value_type = args[2].lower()
                
                try:
                    # value = eval(f"{value_type}('{value}')")
                    value = eval(f"{value_type}({value})")
                except Exception as e:
                    await update.message.reply_text(f"Error converting value: {e} to {value_type}")
                    return           
                
            # Update the persistent bot user data
            context.application.persistence.update_bot_data({key: value})                    
            context.bot_data[key] = value              
            self.app.bot_data[key] = value        
                
            # force persistence storage to save bot data
            await context.application.persistence.flush()        

            await update.message.reply_text(f"Bot data updated: {key} = {value}")
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error_message = f"Error getting user data in {fname} at line {exc_tb.tb_lineno}: {e}"
            self.logger.error(error_message)               
            await update.message.reply_text(error_message, parse_mode=None)

    @with_typing_action
    @with_log_admin
    @with_register_user
    async def set_user_data(self, update: Update, context: CallbackContext) -> None:
        """Command to set user data

        Args:
            update (Update): The update object
            context (CallbackContext): The context object
        """
        try:
            args = context.args
            if len(args) < 2:
                await update.message.reply_text("Please provide both the key and value.\nUsage: /set_user_data <key> <value>")
                return

            key = args[0]
            value = args[1]
            
            # convert type of value according third parameter
            if len(args) > 2 and args[2].lower() not in ["str"]:
                value_type = args[2].lower()

                try:
                    value = eval(f"{value_type}({value})")
                except Exception as e:
                    await update.message.reply_text(f"Error converting value: {e} to {value_type}")
                    return          

            user_id = update.effective_user.id

            # Update the user data  
            # await context.application.persistence.update_user_data(user_id=user_id, data={key: value})           
            context.user_data[key] = value            
            # self.app.user_data[key] = value     
            
            # check
            user_data = await context.application.persistence.get_user_data()       
            user_data = context.user_data         
                
            # force persistence storage to save bot data
            await context.application.persistence.flush()            

            await update.message.reply_text(f"User data updated: {key} = {value}")
            
        except Exception as e:
            self.logger.error(f"Error setting user data: {e}")
            await update.message.reply_text(f"An error occurred while setting user data: {e}")
        
    async def post_init(self, app: Application) -> None:
        """Post-initialization tasks for the bot

        Args:
            app (Application): The application object
        """
        try:
            # check user data
            user_data = await app.persistence.get_user_data()
            
            self.logger.info("Bot post-initialization complete!")
            admin_users = self.config['bot'].get('admin_users', [])
            bot_username = (await app.bot.get_me()).username
            version_message = (
                f"Bot post-initialization complete!\n"
                f"Version: {__version__}\n"
                f"Bot Username: @{bot_username}\n"
                f"Run /help to see available commands."
            )
            
            if admin_users:
                main_script_path = get_main_script_path()
                command_line = " ".join(sys.argv)
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                version_message += (
                    f"\nMain Script Path: {main_script_path}"
                    f"\nCommand Line: {command_line}"
                    f"\nHostname: {hostname}"
                    f"\nIP Address: {ip_address}"
                )
            
            for admin_id in admin_users:
                try:
                    await app.bot.send_message(chat_id=admin_id, text=version_message)
                except Exception as e:
                    self.logger.error(f"Failed to send message to admin {admin_id}: {e}")
            
            # Set bot commands dynamically
            bot_commands = [
                (f"/{cmd}", handler.description)
                for cmd, handler in self.commands.items()
            ]
            await app.bot.set_my_commands(bot_commands)
            my_commands = await app.bot.get_my_commands()
            commands_dict = {
                cmd.command: cmd.description or app.bot.commands[cmd.command].__doc__
                for cmd in my_commands
            }
            self.logger.info(f"Registered commands: {commands_dict}") 
        
            # Initialize the status message flag
            self.status_message_enabled = self._load_status_message_enabled()
            
            # Load send_status_interval from persistent bot data
            self.send_status_interval = self._load_send_status_interval() 
        
            # Add job to send status message every 30 minutes
            job_queue: JobQueue = self.app.job_queue
            job_queue.run_repeating(self.send_status_message, interval=self.send_status_interval, first=0)    
            self.job_queue = job_queue                 
                      
        except Exception as e:
            self.logger.error(f"Error during post-initialization: {e}")

    async def post_stop(self, app: Application) -> None:
        """Post-stop tasks for the bot

        Args:
            app (Application): The application object
        """
        try:
            self.logger.info("Bot is stopping...")
            # Perform any cleanup tasks here
            # For example, save any necessary data or close connections
                
            # check user data
            user_data = await app.persistence.get_user_data()
            
        except Exception as e:
            self.logger.error(f"Error during post-stop: {e}")
            
    async def post_shutdown(self, app: Application) -> None:
        """Post-shutdown tasks for the bot

        Args:
        app (Application): The application object
        """
        try:
            self.logger.info("Bot is shutting down...")
            # Perform any cleanup tasks here
            # For example, save any necessary data or close connections
        
            # check user data
            user_data = await app.persistence.get_user_data()
                            
        except Exception as e:
            self.logger.error(f"Error during post-shutdown: {e}")
            
    def run(self, external_handlers: list) -> None:
        app = Application.builder().token(self.token).build()

        async def get_bot_username():
            bot = await app.bot.get_me()
            return bot.username

        loop = asyncio.get_event_loop()
        bot_username = loop.run_until_complete(get_bot_username())
             
        # get main script path folder
        main_script_path = str(get_main_script_path().parent)
        self.logger.debug(f"The main script folder path is: {main_script_path}")
        persistence = PicklePersistence(filepath=f'{main_script_path}{os.sep}{bot_username}_bot_data', update_interval=2)

        app = Application.builder().token(self.token).persistence(persistence).post_init(post_init=self.post_init).post_stop(post_stop=self.post_stop).post_shutdown(post_shutdown=self.post_shutdown).build()

        # Register command handlers
        for cmd_name in self.commands:
            app.add_handler(TelegramCommandHandler(cmd_name, self.handle_command))

        # Register the list_commands handler
        app.add_handler(TelegramCommandHandler("list_commands", self.handle_list_commands, filters=filters.User(user_id=self.admin_users)))
        
        # Register the Git command handler
        app.add_handler(TelegramCommandHandler("git", self.cmd_git, filters=filters.User(user_id=self.admin_users)))
        
        # Register the restart command handler
        app.add_handler(TelegramCommandHandler("restart", self.restart_bot, filters=filters.User(user_id=self.admin_users)))
        
        # Register the stop command handler
        # app.add_handler(TelegramCommandHandler("stop", self.stop_bot, filters=filters.User(user_id=self.admin_users)))
        app.add_handler(TelegramCommandHandler("stop", self.cmd_stop, filters=filters.User(user_id=self.admin_users)))

        # Register the show_user_data handler
        app.add_handler(TelegramCommandHandler("show_user_data", self.show_user_data, filters=filters.User(user_id=self.admin_users)))
        
        # Register the list_registered_users handler
        app.add_handler(TelegramCommandHandler("users", self.cmd_get_users, filters=filters.User(user_id=self.admin_users)))
        
        # Register the show_version handler
        # app.add_handler(TelegramCommandHandler("version", self.show_version))
        app.add_handler(TelegramCommandHandler("version", self.handle_version))

        # Register the update_library handler
        app.add_handler(TelegramCommandHandler("update_library", self.update_library, filters=filters.User(user_id=self.admin_users)))

        # Register the external handlers
        for handler in external_handlers:
            app.add_handler(TelegramCommandHandler("echo", handler), group=-1)

        # Register the toggle command
        app.add_handler(TelegramCommandHandler('toggle_status', self.toggle_status_message, filters=filters.User(user_id=self.admin_users)))
        
        # Register the change_status_interval command handler
        app.add_handler(TelegramCommandHandler("change_status_interval", self.change_status_interval, filters=filters.User(user_id=self.admin_users)))        

        # Register the call_function_command handler
        app.add_handler(TelegramCommandHandler("call_function", self.call_function_command, filters=filters.User(user_id=self.admin_users)))

        # Register the show_bot_data handler
        app.add_handler(TelegramCommandHandler("show_bot_data", self.show_bot_data, filters=filters.User(user_id=self.admin_users)))        

        # Register the eval_command handler
        app.add_handler(TelegramCommandHandler("eval", self.eval_exec_command, filters=filters.User(user_id=self.admin_users)))      

        # Register the exec_command handler
        app.add_handler(TelegramCommandHandler("exec", self.eval_exec_command, filters=filters.User(user_id=self.admin_users)))

        # Register the set_bot_data handler
        app.add_handler(TelegramCommandHandler("set_bot_data", self.set_bot_data, filters=filters.User(user_id=self.admin_users)))
        
        # register the set_user_bot command handler
        app.add_handler(TelegramCommandHandler("set_user_data", self.set_user_data, filters=filters.User(user_id=self.admin_users)))        

        self.logger.info("Bot started successfully!")
        
        self.app = app
            
        # # Load send_status_interval from persistent bot data
        # self.send_status_interval = self._load_send_status_interval() 
    
        # # Add job to send status message every 30 minutes
        # job_queue: JobQueue = self.app.job_queue
        # job_queue.run_repeating(self.send_status_message, interval=self.send_status_interval, first=0)    
        # self.job_queue = job_queue    
        
        # Call post_init after initializing the bot
        app.run_polling()