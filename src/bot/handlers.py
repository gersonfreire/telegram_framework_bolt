from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import TelegramBotFramework

class CommandHandler:
    def __init__(self, name: str, description: str, response_template: str):
        self.name = name
        self.description = description
        self.response_template = response_template

    async def get_response(self, bot: 'TelegramBotFramework') -> str:
        """Generic command handler to return a response based on the command name

        Args:
            bot (TelegramBotFramework): _description_

        Returns:
            str: Generic response based on the command name
        """
        
        try:
            if self.name == "help":
                my_commands = await bot.app.bot.get_my_commands()
                commands_dict = {
                    cmd.command: cmd.description or bot.commands[cmd.command].__doc__
                    for cmd in my_commands
                }

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

                return self.response_template.format(commands=commands_list)

            elif self.name == "settings":
                return self.response_template.format(settings=bot.settings.display())
            else:
                return self.response_template
            
        except Exception as e:
            # Handle or log the exception as needed
            return f"An error occurred: {str(e)}"