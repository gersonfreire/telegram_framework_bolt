The name you use for importing your package in your code is determined by the structure of your package and the names of the modules within it, not by the name specified in

setup.py

.

Given your current project structure, you will import your modules based on the directory and file names within the

src

 directory. For example, if you have the following structure:

```
src/
│
├── bot/
│   ├── __init__.py
│   ├── core.py
│   ├── handlers.py
│   └── settings.py
```

You would import the modules like this:

```python
from bot.core import TelegramBotFramework
from bot.handlers import CommandHandler
from bot.settings import Settings
```

The

setup.py

 file specifies the package name for distribution purposes, but the import statements in your code depend on the actual directory and module names.

### Example Usage

If you have the following structure:

```
src/
│
├── bot/
│   ├── __init__.py
│   ├── core.py
│   ├── handlers.py
│   └── settings.py
```

Your import statements would look like this:

```python
from bot.core import TelegramBotFramework
from bot.handlers import CommandHandler
from bot.settings import Settings
```

### Summary

- The name specified in

setup.py

 (`tlgbotfwk`) is used for distribution and installation purposes.

- The import statements in your code are based on the directory and module names within the

src

 directory.

So, you will continue to use `from bot.core import TelegramBotFramework` and similar import statements based on your directory structure.
