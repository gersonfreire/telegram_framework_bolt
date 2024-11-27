import os
import re
from pathlib import Path

def read_version(file_path: Path, pattern: str) -> str:
    with file_path.open('r', encoding='utf-8') as file:
        content = file.read()
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    raise ValueError(f"Version not found in {file_path}")

def write_version(file_path: Path, pattern: str, new_version: str) -> None:
    with file_path.open('r+', encoding='utf-8') as file:
        content = file.read()
        new_content = re.sub(pattern, f'\\1{new_version}\\3', content)
        file.seek(0)
        file.write(new_content)
        file.truncate()

def increment_version(version: str) -> str:
    major, minor, patch = map(int, version.split('.'))
    patch += 1
    return f"{major}.{minor}.{patch}"

def update_version_in_files():
    current_script_path = {Path(__file__).parent}
    files_to_update = [
        {
            "path": Path(f"{current_script_path}{os.sep}bot{os.sep}core.py"),
            "pattern": r'(__version__\s*=\s*["\'])([\d.]+)(["\'])'
        },
        {
            "path": Path(f"{current_script_path}{os.sep}..{os.sep}setup.py"),
            "pattern": r'(version\s*=\s*["\'])([\d.]+)(["\'])'
        },
        {
            "path": Path(f"{current_script_path}{os.sep}..{os.sep}pyproject.toml"),
            "pattern": r'(version\s*=\s*["\'])([\d.]+)(["\'])'
        }
    ]

    for file_info in files_to_update:
        file_path = file_info["path"]
        pattern = file_info["pattern"]

        current_version = read_version(file_path, pattern)
        new_version = increment_version(current_version)
        write_version(file_path, pattern, new_version)

        print(f"Updated {file_path} from version {current_version} to {new_version}")

if __name__ == "__main__":
    update_version_in_files()