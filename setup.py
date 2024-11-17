
""" setuptools entry point for the project.

Raises:
    ValueError: _description_
    FileNotFoundError: _description_

Returns:
    _type_: _description_
    
SetuptoolsDeprecationWarning: setup.py install is deprecated.
!!

        ********************************************************************************
        Please avoid running ``setup.py`` directly.
        Instead, use pypa/build, pypa/installer or other
        standards-based tools.

        See https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html for details.
        ********************************************************************************

!!
"""
from setuptools import setup, find_packages

setup(
    name="tlgbotfwk",
    version="0.4.7",
    description='A powerful and extensible Python-based Telegram bot framework',
    author='Maker',
    author_email='youremail@example.com',
    url='https://github.com/gersonfreire/telegram_framework_bolt',  # Replace with your repository URL
    packages=find_packages(),
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