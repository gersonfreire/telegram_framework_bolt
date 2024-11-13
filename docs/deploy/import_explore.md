To find out the correct import names for already installed libraries, you can follow these steps:

1. **Check the Package Documentation**:

   - The PyPI page or the official documentation of the package usually provides the correct import statement.
2. **Use `pip show` Command**:

   - This command provides metadata about the installed package, including the location where it is installed.

   ```sh
   pip show <package-name>
   ```
3. **Explore the Installed Package Directory**:

   - Navigate to the site-packages directory where the package is installed and look at the folder names.

   ```sh
   python -m site
   ```

   - This command will show you the site-packages directory. You can then navigate to this directory and list its contents to see the installed packages.
4. **Use Python's `help()` Function**:

   - Start a Python interactive shell and use the `help()` function to explore the package.

   ```python
   import <package-name>
   help(<package-name>)
   ```
5. **Check `pip list`**:

   - This command lists all installed packages. You can use it to verify that the package is installed.

   ```sh
   pip list
   ```

For example, if you have installed `telegram-bot-framework-bolt`, you can use the following commands to find out the correct import name:

```sh
pip show telegram-bot-framework-bolt
```

```sh
python -m site
```

```sh
pip list
```

In the Python interactive shell:

```python
import telegram_bot_framework_bolt
help(telegram_bot_framework_bolt)
```

These steps should help you determine the correct import name for the installed package.
