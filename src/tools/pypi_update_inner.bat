@echo on

echo Running setup.py
python setup.py sdist bdist_wheel
@REM pause

echo Uploading to PyPI
twine upload --repository-url https://upload.pypi.org/legacy/ dist/* --non-interactive --username __token__ --password %PYPI_API_TOKEN%