import os
import subprocess
import sys
from dotenv import load_dotenv

def activate_virtualenv():
    """Activate the virtual environment."""
    if os.name == 'nt':
        activate_script = os.path.join('.venv', 'Scripts', 'activate.bat')
    else:
        activate_script = os.path.join('.venv', 'bin', 'activate')
    
    if not os.path.exists(activate_script):
        raise FileNotFoundError(f"Virtual environment activation script not found: {activate_script}")
    
    return activate_script

def run_command(command, shell=False):
    """Run a command and check for errors."""
    result = subprocess.run(command, shell=shell, check=True, text=True)
    return result

def main():
    # Load environment variables from .env file
    load_dotenv('.env')

    # Activate the virtual environment
    activate_script = activate_virtualenv()
    if os.name == 'nt':
        run_command(f'call {activate_script}', shell=True)
    else:
        run_command(f'source {activate_script}', shell=True)

    # Generate the source distribution and built distribution
    print("Running setup.py")
    run_command([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])

    # Upload the package to PyPI
    print("Uploading to PyPI")
    pypi_token = os.getenv('PYPI_API_TOKEN')
    if not pypi_token:
        raise EnvironmentError("PYPI_API_TOKEN environment variable not set")

    run_command([
        'twine', 'upload', '--repository-url', 'https://upload.pypi.org/legacy/', 'dist/*',
        '--non-interactive', '--username', '__token__', '--password', pypi_token
    ])

if __name__ == '__main__':
    main()