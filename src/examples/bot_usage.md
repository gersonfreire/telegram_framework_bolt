# Usage Guide for Host Watch Bot

Welcome to the Host Watch Bot! This bot is designed to monitor remote hosts and provide various utilities through Telegram commands. Below is a comprehensive list of available commands, along with their descriptions and usage instructions.

## Available Commands

### Admin-Only Commands (👑)
These commands are restricted to admin users. Ensure you have the necessary permissions to use them.

- **/call_function**: Dynamically call a function.
- **/change_ping_port_command**: Change the TCP port checked by the scheduled task of pinging a host.
- **/change_status_interval**: Change the interval for sending status messages and restart the job.
- **/eval**: Evaluate a Python expression.
- **/exec**: Execute a Python command.
- **/execute_command**: Execute a command on the host operating system and return the result.
- **/execute_ssh_command**: Execute an SSH command on the remote host using stored credentials and return the result.
- **/git**: Update the bot's version from a git repository.
- **/list_commands**: List all available commands.
- **/list_failures**: List each host and its last failure date.
- **/ping_add**: Add a new host to be monitored by the bot.
- **/ping_delete**: Remove a host from the bot's monitoring list.
- **/ping_host_command**: Check if a host is up or down.
- **/ping_host_port_command**: Ping a host by name or IP address and TCP port number.
- **/ping_interval**: Change the interval to check a monitored host.
- **/ping_list**: List the hosts being monitored by the bot.
- **/ping_log**: View the log of ping attempts (details not specified).
- **/restart**: Restart the bot.
- **/set_bot_data**: Set data for the bot.
- **/set_user_data**: Set data for a user.
- **/show_bot_data**: Show current bot data in JSON format.
- **/show_user_data**: Show current persistent user data.
- **/stop**: Stop the bot (details not specified).
- **/store_credentials**: Store username and password associated with a host or show existing credentials if no parameters are provided.
- **/toggle_status**: Toggle the status message on or off to indicate whether the bot is active.
- **/update_library**: Update the `tlgbotfwk` library.
- **/users**: List all registered users.

### General Commands
These commands are available to all users:

- **/echo**: A generic handler for echoing user messages.
- **/help**: Display available commands and their descriptions.
- **/settings**: Manage bot settings.
- **/start**: Initialize the bot and display a welcome message.
- **/version**: Show the current version of the bot.

## How to Use Commands

1. **Invoke the Bot**: Start a conversation with the bot in Telegram.
2. **Type a Command**: Enter any of the commands listed above, prefixed with a `/`. For example, to check if a host is up, type `/ping_host_command <host_name>`.
3. **Follow Prompts**: Some commands may require additional parameters (like host names or port numbers). Follow the prompts or usage instructions provided by the bot.

### Note on Admin Commands
Commands marked with a crown icon (👑) are exclusive to admin users. If you attempt to use these commands without the necessary permissions, the bot will inform you that you do not have access.

## Conclusion
This bot provides a powerful way to monitor hosts and manage various tasks through Telegram. Make sure to familiarize yourself with the commands and their usage to get the most out of your experience!

For further assistance, refer to the [README.md](README.md) for more detailed information about the bot's features and setup.