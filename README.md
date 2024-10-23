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