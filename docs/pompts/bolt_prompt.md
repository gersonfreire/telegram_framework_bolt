

Create an entire python framework to build telegram bots that offers embedded basic commands described in this bot_usage.md file uploaded here plus users management, payment and balance management for this users and settings management.

You must implement a python super class which inherits from  base classes of python-telebra-bot latest version library.

This framework must implement by default the embeded bot persistence which sotres all state of the bot that will be autmatically reloaded at bot start, included bot users data as each user name, id and balance. All embeded commands must be automatically inherited when the programmer creates a script from this framework, as simple as instantiting the main class like this single line of code: bot = MyTelegramFramework().

Embed also a command to schedule tasks

Please use the native persistence already exists in python-telegram-bot if not please adjust all code to use the Application.builder().persistence embeded which is a pickle persistence

Also create a examples folder whith new python example for an echo bot using this framework inside the examples folder and another example showing how to create a bot using the scheduling embeded functionality
