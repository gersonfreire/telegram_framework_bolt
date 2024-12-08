import os
import sys
from typing import TYPE_CHECKING
from telegram.ext import filters, Application, ContextTypes

import telegram

if TYPE_CHECKING:
    from .core import TelegramBotFramework

class CommandHandler:
    def __init__(self, name: str, description: str, response_template: str):
        self.name = name
        self.description = description
        self.response_template = response_template

    async def get_response(self, bot: 'TelegramBotFramework', update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Generic command handler to return a response based on the command name

        Args:
            bot (TelegramBotFramework): _description_

        Returns:
            str: Generic response based on the command name
        """
        
        try:
            # TODO: show admin commands only to admin users
            if self.name == "help":
                my_commands = await bot.app.bot.get_my_commands()
                commands_dict = {
                    cmd.command: cmd.description or bot.commands[cmd.command].__doc__
                    for cmd in my_commands
                }                
                
                # get all handlers from application object and get the filters of each handler                
                global_handlers = await self.get_handlers_by_user(bot.app)
                
                # Get list of command names from global_handlers dictionary
                # Initialize user_commands_from_handlers as a dictionary
                user_commands_from_handlers = {}       
                help_text_from_handlers = '' 
                
                # Sort the global_handlers dictionary by handler['command']
                for user_id in global_handlers:
                    global_handlers[user_id] = sorted(global_handlers[user_id], key=lambda x: x['command'])
                        
                for user_id, handlers in global_handlers.items():
                    if user_id == 0 or user_id == update.effective_user.id:
                        for handler in handlers:
                            try:
                                # TODO: check if the command is already in the user_commands_from_handlers dictionary
                                # if not, add it to the dictionary
                                if handler['command'] not in user_commands_from_handlers:
                                    user_commands_from_handlers[handler['command']] = handler['handler_info']
                                
                                    # Set a crown at the help commands list to show which commands are admins
                                    if user_id == update.effective_user.id and update.effective_user.id in bot.admin_users:
                                        help_text_from_handlers += f"👑 /{handler['command']} - {handler['handler_info']['docstring'][0]}\n"
                                    else:
                                        help_text_from_handlers += f"/{handler['command']} - {handler['handler_info']['docstring'][0]}\n"
                                    
                            except Exception as e:
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                self.logger.error(f"Error processing command handler in {fname} at line {exc_tb.tb_lineno}: {e}")
                                        
                # Get menu commands for the first admin user of admin list
                admin_commands = await bot.app.bot.get_my_commands(scope={'type': 'chat', 'chat_id': bot.admin_users[0]}) if bot.admin_users else [] 

                commands_list = "\n".join(
                    f"/{cmd} - {handler.description}"
                    for cmd, handler in bot.commands.items()
                )

                registered_commands = "\n".join(
                    f"/{cmd} - {handler['docstring']}"
                    for cmd, handler in bot.registered_handlers.items()
                    if cmd not in bot.commands
                )

                commands_list += "\n" + registered_commands
                
                # TODO: clear telegram command menu and insert the commands from the handlers
                # Clear the current command menu
                await bot.app.bot.delete_my_commands()

                # Insert the commands from the handlers into the telegram menu command
                new_commands = [
                    telegram.BotCommand(command=cmd, description=handler['docstring'][0])
                    for cmd, handler in user_commands_from_handlers.items()
                ]
                await bot.app.bot.set_my_commands(new_commands)
                
                # new_commands = await bot.app.bot.get_my_commands()

                # TODO: wait for stable version to be aproved and remove the commented lines
                # Legacy: using the commands dictionary to return the help text
                # return self.response_template.format(commands=commands_list)
                # New: using the text generated from handlers to return the help text
                return self.response_template.format(commands=help_text_from_handlers)

            elif self.name == "settings":
                return self.response_template.format(settings=bot.settings.display())
            elif self.name == "echo":
                return self.response_template.format(message='echo')
            elif self.name == "start":
                return self.response_template.format(bot_username=f'@{bot.app.bot.username}', version=bot.version, user_id=update.effective_user.id, username=update.effective_user.username if update.effective_user.username else '[unknown user name]')
            else:
                return self.response_template
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error_message = f"Error getting user data in {fname} at line {exc_tb.tb_lineno}: {e}"
            self.logger.error(error_message)               
            await update.message.reply_text(error_message, parse_mode=None)           
            
    async def get_handlers_by_user(self, app: 'Application') -> str:
        """Get all the filters from the registered handlers

        Args:
            app (Application): _description_

        Returns:
            str: List of filters
        """
        
        try:
            commands_by_user = {}
            
            for handler in app.handlers.values():
                for sub_handler in handler:
                    try:
                        if isinstance(sub_handler, telegram.ext.CommandHandler):
                            
                            # get the function name and docstring that implement this command handler callback
                            callback_func = sub_handler.callback
                            func_name = callback_func.__name__
                            docstring = callback_func.__doc__.split(f'\n\n') if callback_func.__doc__ else "No description available"
                            handler_info = {"function": func_name, "docstring": docstring}
                            
                            if isinstance(sub_handler.filters, filters.User):                                  
                                for user_id in list(sub_handler.filters.user_ids):
                                    if user_id not in commands_by_user:
                                        commands_by_user[user_id] = []
                                    for command in list(sub_handler.commands):
                                        if command not in commands_by_user[user_id]:      
                                            command_dict = {
                                                'command':command,
                                                'handler_info': handler_info
                                            }                                      
                                            commands_by_user[user_id].append(command_dict)
                            else:                              
                                if 0 not in commands_by_user:
                                    commands_by_user[0] = []
                                for command in list(sub_handler.commands):
                                    if command not in commands_by_user[0]:      
                                        command_dict = {
                                            'command':command,
                                            'handler_info': handler_info
                                        }                                                 
                                        commands_by_user[0].append(command_dict)                                
                            
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        self.logger.error(f"Error processing handler filters in {fname} at line {exc_tb.tb_lineno}: {e}")
                
            return commands_by_user
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logger.error(f"Error getting user data in {fname} at line {exc_tb.tb_lineno}: {e}")             