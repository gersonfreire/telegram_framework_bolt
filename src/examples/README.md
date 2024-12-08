# Telegram Bot Framework Test

This is a Proof of Concept (POC) for the [Telegram Bot Framework](https://github.com/gersonfreire/telegram_framework_bolt) which in turn is the new and stable version of this [legacy](https://github.com/gersonfreire/telegram-bot-framework) framework

[Telegram Bot Framework](https://github.com/gersonfreire/telegram_framework_bolt) is a powerful and extensible Telegram bot framework designed for monitoring remote hosts and providing various utilities. This project leverages the `python-telegram-bot` library and provides a simple way to create and manage Telegram bots.

## Features

- Echo user messages
- Load environment variables
- Easy to extend with custom commands
- Configuration via YAML files

## Requirements

- Python 3.6+
- `python-telegram-bot` library
- `python-dotenv` library
- `PyYAML` library

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/gersonfreire/tlgfwk_test.git

   ```

   `cd <my-clone-folder>`
2. **Create a virtual environment**:

   `python -m venv venv`
3. **Activate the virtual environment**:

   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
4. **Install the dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

   *Obs.: if you already have the library installed, pelase ensure you have the latest version with command:*

   ```
   pip install --upgrade tlgbotfwk
   ```

## Configuration

1. Create a.env file in the root directory and add your bot token:

```env
   DEFAULT_BOT_TOKEN=your-telegram-bot-token
```

2. Edit the config.yml file to configure your bot settings:

```yml
   bot:
     default_bot_token: "your-telegram-bot-token"
     name: "MyTelegramBot"
     description: "A powerful and extensible Telegram bot framework"
     admin_users:
       - your-telegram-user-id
     commands:
       start:
         description: "Start the bot"
         response: "Welcome! I'm here to help you. Use /help to see available commands."
       help:
         description: "Show available commands"
         response: "Available commands:\n{commands}"
       settings:
         description: "Manage bot settings"
         response: "Current Settings:\n{settings}"
       echo:
         description: "Echo the user's message"
         response: ""
```

## Usage

1. **Run the bot**:

   ```sh
   python main.py
   ```
2. **Interact with the bot**:

   - Open Telegram and search for your bot.
   - Start a conversation and use the commands defined in config.yml

## Deployment

To deploy the bot, you can use any cloud service that supports Python applications, such as Heroku, AWS, or Google Cloud. Here is an example of how to deploy to Heroku:

1. **Create a `Procfile`** in the root directory:

   ```Procfile
   web: python main.py
   ```
2. **Login to Heroku**:

   ```sh
   heroku login
   ```
3. **Create a new Heroku app**:

   ```sh
   heroku create mytelegrambot
   ```
4. **Push the code to Heroku**:

   ```sh
   git push heroku main
   ```
5. **Set the environment variables on Heroku**:

   ```sh
   heroku config:set DEFAULT_BOT_TOKEN=your-telegram-bot-token
   ```
6. **Open the app**:

   ```sh
   heroku open
   ```

## Examples

In folder ` src\examples` there is a couple of examples which is under construction like this framework, but the `host_watch_bot.py `sample is becoming interesting.

This bot provides a powerful way to monitor hosts and manage various tasks through Telegram. Make sure to familiarize yourself with the commands and their usage to get the most out of your experience!

For further assistance, refer to the [bot usage guide](src/examples/bot_usage.md) for more detailed information about the bot's features and setup.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

***Make sure to replace placeholders like `your-telegram-bot-token` and `yourusername` with your actual bot token and GitHub username.Make sure to replace placeholders like `your-telegram-bot-token` and `yourusername` with your actual bot token and GitHub username.***

---
