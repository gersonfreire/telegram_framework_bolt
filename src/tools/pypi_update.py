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
    try:
        result = subprocess.run(command, shell=shell, check=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with return code {e.returncode}")
        print(f"Output: {e.output}")
        # raise
        return None

def main():
    # Load environment variables from .env file in the current script folder    
    if load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), override=True):
        print("Environment variables loaded successfully")
        pypi_token = os.getenv('PYPI_API_TOKEN')
    else:
        print("Failed to load environment variables")
        return

    # Activate the virtual environment
    activate_script = activate_virtualenv()
    if os.name == 'nt':
        run_command(f'call {activate_script}', shell=True)
    else:
        run_command(f'source {activate_script}', shell=True)

    # Generate the source distribution and built distribution
    print("Running setup.py")
    result = run_command([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])
    if result is None:
        print("Failed to generate the distribution files")
        return

    # Upload the package to PyPI
    print("Uploading to PyPI")
    if not pypi_token:
        raise EnvironmentError("PYPI_API_TOKEN environment variable not set")

    result = run_command([
        'twine', 'upload', '--repository-url', 'https://upload.pypi.org/legacy/', 'dist/*',
        '--non-interactive', '--username', '__token__', '--password', pypi_token
    ])
    if result is None:
        print("Failed to upload the package to PyPI")
        return
    
    print("Package uploaded successfully")

if __name__ == '__main__':
    main()