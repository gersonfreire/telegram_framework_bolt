@echo on

cd ..\..
@REM pause

call .venv\Scripts\activate.bat
@REM pause

echo Running setup.py
python setup.py sdist bdist_wheel
@REM pause

echo Loading environment variables from .env file
@REM dotenv -f .\.env
dotenv -f .env -- cmd /c "call pypi_update_inner.bat"

echo Uploading to PyPI
twine upload --repository-url https://upload.pypi.org/legacy/ dist/* --non-interactive --username __token__ --password %PYPI_API_TOKEN%

pause
