import os

EXCLUDE_DIRS = {
    "venv", "__pycache__", ".git", ".mypy_cache", ".pytest_cache", ".idea", ".vscode", ".DS_Store", ".env"
}
EXCLUDE_FILES = {
    ".DS_Store", ".env"
}

def print_tree(start_path, indent=""):
    for item in sorted(os.listdir(start_path)):
        if item in EXCLUDE_DIRS or item in EXCLUDE_FILES:
            continue
        path = os.path.join(start_path, item)
        if os.path.isdir(path):
            print(f"{indent}📁 {item}/")
            print_tree(path, indent + "│   ")
        else:
            print(f"{indent}📄 {item}")

# Replace this with your backend directory
backend_root = "."
print(f"Project structure for: {backend_root}/\n")
print_tree(backend_root)
