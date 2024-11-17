Sure, let's create a `setup.py` file for your project and go through the steps to deploy it to PyPI.

### Step 1: Create `setup.py`

Create a `setup.py` file in the root directory of your project with the following content:

```python
from setuptools import setup, find_packages

setup(
    name='tlgbotfwk',
    version='0.4.10',  # Incremented version
    description='A powerful and extensible Python-based Telegram bot framework

',


    author='Maker',
    author_email='youremail@example.com',
    url='https://github.com/gersonfreire/telegram_framework_bolt',  # Replace with your repository URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
```

### Step 2: Create `pyproject.toml`

Create a `pyproject.toml` file in the root directory of your project with the following content:

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "tlgbotfwk"
version = "0.4.10"
description = "A powerful and extensible Python-based Telegram bot framework"
authors = [
    { name = "Maker", email = "youremail@example.com" }
]
dependencies = [
    "python-telegram-bot>=20.7",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0.1",
]
requires-python = ">=3.6"
```

### Step 3: Create Distribution Packages

1. **Ensure you have the necessary tools**:

   ```sh
   pip install setuptools wheel
   ```
2. **Create the distribution files**:

   ```sh
   python setup.py sdist bdist_wheel
   ```

   This will generate distribution files in the `dist` directory.

### Step 4: Upload to PyPI

1. **Install `twine`**:

   ```sh
   pip install twine
   ```
2. **Upload the distribution files to PyPI**:

   ```sh
   twine upload dist/*
   ```

   You will be prompted to enter your PyPI username and password. If you are using an API token, set the `TWINE_USERNAME` to `__token__` and `TWINE_PASSWORD` to your API token.

### Example Commands

Here is a summary of the commands you will run:

```sh
# Step 1: Create setup.py and pyproject.toml (done manually)

# Step 2: Install necessary tools
pip install setuptools wheel

# Step 3: Create distribution files
python setup.py sdist bdist_wheel

# Step 4: Install twine
pip install twine

# Step 5: Upload to PyPI
twine upload dist/*
```

### Additional Notes

- Ensure that your

README.md

 and

LICENSE

 files are in the root directory of your project, as they will be included in the distribution.

- If you encounter any issues, refer to the [Python Packaging User Guide](https://packaging.python.org/) for more detailed instructions and troubleshooting tips.

By following these steps, you can package and deploy your project to PyPI.
