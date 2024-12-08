<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/FxL5qM0.jpg" alt="Bot logo"></a>
</p>

# Telegram Bot Framework

A powerful and extensible Python-based Telegram bot framework that provides automatic command handling, settings management, and easy configuration.

This is an updated and totally rewritten from ground of a [legacy version](https://github.com/gersonfreire/telegram-bot-framework)

## About

You can find many libraries and modules ready to build bots on Telegram, but none of them cover the basic functionalities that are almost indispensable, such as creating a help menu automatically from commands, registering users, generating a log in the Telegram administrator and others. The purpose of this library is to fill these gaps and allow Telegram bot developers to quickly create powerful, stable and secure bots in just a few lines of code. This work is still in its early stages, but I invite you to help me explore and conquer the fascinating world of Telegram bots by collaborating and using this library.

The orginal article in English is here: [A Python Framework for Telegram Bots - DEV Community](https://dev.to/gersonfreire/a-python-framework-for-telegram-bots-238f)

The orginal article in Portuguese is here: [Biblioteca em nível de aplicação para criar bots no Telegram 🤖 · telegram · TabNews](https://www.tabnews.com.br/telegram/biblioteca-de-nivel-de-aplicativo-para-criar-bots-no-telegram)

## How it works

Basically, we build a class called *TelegramBotFramework*, which inherits from the *python-telegram-bot Application class*, implemented by the telegram.ext library, provided by the python-telegram-bot package, version 21 or greater ([https://github.com/python-telegram-bot/python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)). In this child class, we implement some default methods to handle the universal commands /start, /help and other unrecognized commands. However, the developer can implement their own command handlers without losing the built-in functionality. I recommend reading the source code for more details. I also recommend Python 3.12 version.

## Features

- 🚀 Automatic command handling
- ⚙️ Built-in settings management
- 📝 YAML-based configuration
- 🔒 Environment variable support
- 📚 Easy to extend and customize

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/telegram-bot-framework.git
cd telegram-bot-framework
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the bot:

   - Copy `.env.example` to `.env` and add your bot token
   - Copy `config.yml.example` to `config.yml` and customize as needed
5. Run the bot:

```bash
python main.py
```

## Importing

```python
from bot.core import TelegramBotFramework
from bot.handlers import CommandHandler
from bot.settings import Settings
```

## Project Structure

```
├── src/
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── handlers.py
│   │   └── settings.py
│   └── main.py
├── .env.example
├── .gitignore
├── config.yml.example
├── requirements.txt
└── README.md
```

## Configuration

 Environment Variables

Create a `.env` file in the root directory and add your bot token and admin user IDs:

```
DEFAULT_BOT_TOKEN=your_bot_token_here
ADMIN_ID_LIST=your_telegram_user_id_here
```

### Config File (config.yml)

The `config.yml` file contains bot settings and command configurations:

```yaml
bot:
  name: "MyTelegramBot"
  commands:
    start:
      description: "Start the bot"
      response: "Welcome message"
    help:
      description: "Show available commands"
      response: "Available commands:\n{commands}"
    settings:
      description: "Manage bot settings"
      response: "Current Settings:\n{settings}"
    echo:
      description: "Echo the user's message"
      response: "{message}"
    stop:
      description: "Stop the bot"
      response: "Bot stopped."
    version:
      description: "Show bot version"
      response: "Bot version: {version}"
    toggle_status:
      description: "Toggle status message"
      response: "Status message toggled."
    change_status_interval:
      description: "Change status message interval"
      response: "Status message interval changed."
    call_function:
      description: "Call a function"
      response: "Function called."
```

## Available Commands

- `/start` - Initialize the bot
- `/help` - Display available commands
- `/settings` - Show current bot settings
- `/echo` - Echo the user's message
- `/stop` - Stop the bot
- `/version` - Show bot version
- `/toggle_status` - Toggle status message
- `/change_status_interval` - Change status message interval
- `/call_function` - Call a function

* `/eval` - Evaluate a Python expression `(`*new*)
* `/exec` - Execute Python code `(`*new*)

## Extending the Framework

To add new commands, update the `config.yml` file or use the `register_command` method:

```python
bot.register_command(
    name="custom",
    description="A custom command",
    response="Custom response"
)
```

## Examples

In folder ` src\examples` there is a couple of examples which is under construction like this framework, but the `host_watch_bot.py `sample is becoming interesting.

This bot provides a powerful way to monitor hosts and manage various tasks through Telegram. Make sure to familiarize yourself with the commands and their usage to get the most out of your experience!

For further assistance, refer to the [bot usage guide](src/examples/bot_usage.md) for more detailed information about the bot's features and setup.

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Deploy library to *Pypi* (Optional)

* If you do not have setuptools library already installed, you must run this command in order to create the distribution package using *setup.py*:

```bash
pip install setuptools
```

* Additionally, if you do not have the *twine* tool, you will need to install it because it is the tool that uploads your package to *Pypi*:

```bash
pip install twine
```

* Now, if already have *setuptools* installed, generate the package, check the version and other desired details on *setup.py* file and execute the following command to create the distribution folder locally:

```bash
python setup.py sdist bdist_wheel
```

* Finally, upload the distribution package to *Pypi* with the following command, which will ask for the *Pypi* API token:

```bash
twine upload dist/*
```

* After deployed, your library can be installed anywhere with command, where `<library-name>` is the name set on setup.py:

```bash
pip install <library-name>
```

## TODOS:

* [X] Embed persistence to the bot framework
* [X] Embed the settings into the bot framework
* [ ] Set a crown at the help commands list to show which commands are admins'
* [ ] Add a method to change settings
* [ ] Add a command to display the settings
* [ ] Add a command to stop the bot
* [ ] Embed the logging into the bot framework
* [ ] Add type hints to the class methods
* [ ] Add docstrings to the class methods
