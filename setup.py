from setuptools import setup, find_packages

setup(
    name='telegram-bot-framework-bolt',  # Replace with your own package name
    version='0.1.0',
    description='A powerful and extensible Python-based Telegram bot framework',
    author='Maker',
    author_email='youremail@example.com',
    url='https://github.com/gersonfreire/telegram_framework_bolt',  # Replace with your repository URL
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