from setuptools import setup, find_packages

setup(
    name='tlgbotfwk',
    version='0.4.12',  # Incremented version
    description='A powerful and extensible Python-based Telegram bot framework',
    author='Maker',
    author_email='youremail@example.com',
    url='https://github.com/gersonfreire/telegram_framework_bolt',  # Replace with your repository URL
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)