from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import TelegramBotFramework

class CommandHandler:
    def __init__(self, name: str, description: str, response_template: str):
        self.name = name
        self.description = description
        self.response_template = response_template

    def get_response(self, bot: 'TelegramBotFramework') -> str:
        if self.name == "help":
            commands_list = "\n".join(
                f"/{cmd} - {handler.description}"
                for cmd, handler in bot.commands.items()
            )
            return self.response_template.format(commands=commands_list)
        elif self.name == "settings":
            return self.response_template.format(settings=bot.settings.display())
        else:
            return self.response_template