
@REM This script is used to run the bot in the Windows environment

@REM Go to current directory
cd %~dp0

cd ..\..\

@REM Activate the virtual environment and run the bot
call .venv\Scripts\Activate

@REM Run the bot script repassing the arguments
python -m src.examples.host_watch_bot %*
