

Looking at the current implementation, while it has a solid foundation for command handling through the `CommandRegistry` class, it doesn't yet have a proper plugin system for external command handlers. Let's implement a plugin system that allows developers to easily add their own command handlers through external plugins.

Implement Plugin System

* Create

  `src/framework/plugins.py`

* Update

  `src/framework/base.py`

* Create

  `examples/example_plugin.py`

* Update

  `src/main.py`

* Update

  `README.md`

I've implemented a comprehensive plugin system that allows for easy extension of the bot's functionality. Here are the key features:

1. **Plugin Base Class** : A base class that all plugins must inherit from, providing a consistent interface.
2. **Plugin Manager** : Handles loading plugins from files and directories, managing plugin lifecycle.
3. **Automatic Command Registration** : Commands from plugins are automatically registered with the bot.
4. **Hot Loading** : Plugins can be loaded from a directory at runtime.
5. **Example Plugin** : Included an example plugin showing how to create custom commands.

To use the plugin system:

1. Create a plugin by inheriting from `PluginBase`
2. Implement required methods: `name`, `version`, `initialize`, and `get_commands`
3. Place your plugin file in the plugins directory
4. The framework will automatically load and register your plugin's commands

The plugin system is now fully integrated with the existing command registry and supports both user and admin commands from plugins.

Would you like me to explain any specific part of the implementation in more detail?
