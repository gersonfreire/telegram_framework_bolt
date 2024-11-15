# Telegram Bot Framework

A powerful and extensible Python-based Telegram bot framework that provides automatic command handling, settings management, and easy configuration.

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
python src/main.py
```

## Importing

```
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

### Environment Variables

- `BOT_TOKEN`: Your Telegram bot token from BotFather

### Config File (config.yml)

The `config.yml` file contains bot settings and command configurations:

```yaml
bot:
  name: "MyTelegramBot"
  commands:
    start:
      description: "Start the bot"
      response: "Welcome message"
    # Add more commands...
```

## Available Commands

- `/start` - Initialize the bot
- `/help` - Display available commands
- `/settings` - Show current bot settings

## Extending the Framework

To add new commands, update the `config.yml` file or use the `register_command` method:

```python
bot.register_command(
    name="custom",
    description="A custom command",
    response="Custom response"
)
```

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

`pip install setuptools`

* Additionally, if you do not have the *twine* tool, you will need to install it because it is the tool that uploads your package to *Pypi*:

`pip install twine `

* Now, if already have *setuptools* installed, generate the package, check the version and other desired details on *setup.py* file and execute the following command to create the distribution folder locally:

`python setup.py sdist bdist_wheel `

* Finally, upload the distribution package to *Pypi* with the following command, which will ask for the *Pypi* API token:

`twine upload dist/* `

* After deployed, your library can be installed anywhere with command, where `<library-name>` is the name set on setup.py:

`pip install <library-name> `

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
