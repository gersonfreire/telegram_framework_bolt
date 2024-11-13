
To create a `setup.py` file for your project, you need to include the necessary metadata and dependencies. Here is an example `setup.py` file for your Telegram bot framework project:

```python
from setuptools import setup, find_packages

setup(
    name='telegram-bot-framework',
    version='0.1.0',
    description='A powerful and extensible Python-based Telegram bot framework',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/telegram-bot-framework',  # Replace with your repository URL
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'python-telegram-bot>=20.7',
        'python-dotenv>=1.0.0',
        'pyyaml>=6.0.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
```

### Explanation

- **name**: The name of your package.
- **version**: The current version of your package.
- **description**: A short description of your package.
- **author**: The name of the author.
- **author_email**: The email of the author.
- **url**: The URL of the package's repository.
- **packages**: Automatically find all packages in the

src

 directory.

- **package_dir**: Specify that the packages are located in the

src

 directory.

- **install_requires**: A list of dependencies required by the package.
- **classifiers**: A list of classifiers that provide some additional metadata about the package.
- **python_requires**: Specifies the Python versions supported by the package.

### Steps to Create Source and Wheel Distribution

1. **Ensure you have the necessary tools**: Make sure you have `setuptools` and `wheel` installed.

   ```sh
   pip install setuptools wheel
   ```
2. **Create the distribution files**: Run the following command to create source and wheel distributions.

   ```sh
   python setup.py sdist bdist_wheel
   ```

This will generate distribution files in the `dist` directory, which you can then upload to PyPI or TestPyPI using `twine`.

3. **Upload to PyPI**: Use `twine` to upload your package to PyPI.

   ```sh
   pip install twine
   twine upload dist/*
   ```
4. **Enter your PyPI credentials**: You will be prompted to enter your PyPI username and password.

This `setup.py` file and the steps provided will help you package and distribute your Telegram bot framework project.
