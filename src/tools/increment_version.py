import os
import re
from pathlib import Path

def read_version(file_path: Path, pattern: str) -> str:
    with file_path.open('r', encoding='utf-8') as file:
        content = file.read()
        match = re.search(pattern, content)
        if match:
            return match.group(2),content
    raise ValueError(f"Version not found in {file_path}")

def write_version(file_path: Path, pattern: str, new_version: str, current_content:str, current_version:str) -> None:
    with file_path.open('r+', encoding='utf-8') as file:
        content = file.read()
        # new_content = re.sub(pattern, rf'\1{new_version}\3', content)
        new_content = current_content.replace(current_version, new_version)
        file.seek(0)
        file.write(new_content)
        file.truncate()

def increment_version(version: str) -> str:
    major, minor, patch = map(int, version.split('.'))
    patch += 1
    return f"{major}.{minor}.{patch}"

def update_version_in_files():
    current_script_path = f'{Path(__file__).parent}{os.sep}..{os.sep}'
    files_to_update = [
        {
            "path": Path(f"{current_script_path}bot{os.sep}core.py"),
            "pattern": r'(__version__\s*=\s*["\'])([\d.]+)(\s*.*["\'])'
            # __version__ = "0.4.57 chore: Update version to 0.4.55 and refactor version string"
        },
        {
            "path": Path(f"{current_script_path}..{os.sep}setup.py"),
            "pattern": r'(version\s*=\s*["\'])([\d.]+)(\s*.*["\'])'
        },
        {
            "path": Path(f"{current_script_path}..{os.sep}pyproject.toml"),
            "pattern": r'(version\s*=\s*["\'])([\d.]+)(["\'])'
        }
    ]

    for file_info in files_to_update:
        file_path = Path(str(file_info["path"]))
        pattern = file_info["pattern"]

        current_version, current_content = read_version(file_path, pattern)
        new_version = increment_version(current_version)
        write_version(file_path, pattern, new_version, current_content, current_version)

        print(f"Updated {file_path} from version {current_version} to {new_version}")

if __name__ == "__main__":
    update_version_in_files()