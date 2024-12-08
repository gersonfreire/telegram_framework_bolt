
@REM This script is used to run the bot in the Windows environment

@echo on

@REM Go to current directory
cd %~dp0

cd ..\..\

@REM Activate the virtual environment and run the bot
call .venv\Scripts\Activate

cd 
@REM c:\Users\gerson\source\repos\pvt\telegram_framework_bolt

@REM Run the bot script repassing the arguments
python -m src.examples.host_watch_bot %*
