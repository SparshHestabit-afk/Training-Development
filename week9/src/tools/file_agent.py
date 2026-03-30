import os
import json
import pandas as pd

BASE_DIR = "src/files"

class FileAgent:

    SYSTEM_PROMPT = """
        You are file_agent.
        ROLE:
        File system operations specialist.
        CAPABILITIES:
        - create, read, write, delete files
        - list directories
        - check file existence
        RULES:
        1. Only operate inside 'src/files/' directory
        2. Never access outside paths
        3. Always normalize paths
        4. Always ensure directory exists before writing
        5. Never generate content yourself
        BEHAVIOR:
        - deterministic
        - no hallucination
    """

    # PATH CLEANING
    def _clean_path(self, path):
        if not path:
            return None

        path = path.strip()
        # Remove any absolute or repeated prefixes
        path = path.replace("src/files/", "")
        path = path.replace("files/", "")
        path = path.lstrip("/")

        return path

    # FILE TYPE ROUTING
    def _get_category(self, filename):
        ext = filename.split(".")[-1].lower()

        if ext == "py":
            return "codes"
        elif ext == "csv":
            return "data"
        elif ext in ["txt", "pdf", "md"]:
            return "documents"
        elif ext in ["db", "sqlite"]:
            return "databases"
        return "documents"

    # FINAL PATH RESOLUTION
    def _resolve_full_path(self, path=None, filename=None):
        raw = path or filename
        if not raw:
            raise ValueError("No path or filename provided")

        # CRITICAL FIX → ignore directories completely
        raw = self._clean_path(raw)
        filename = os.path.basename(raw)
        category = self._get_category(filename)
        full_path = os.path.join(BASE_DIR, category, filename)

        full_path = os.path.abspath(full_path)
        base_fix = os.path.abspath(BASE_DIR)

        if not full_path.startswith(base_fix):
            raise ValueError("Access outside allowed directory")
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        return full_path

    # MAIN ENTRY
    def handle_task(self, step, query, client, model):
        action = step.get("action")
        args = step.get("args", {})

        args.pop("content", None) if action == "create_file" else None
        if not hasattr(self, action):
            return f"Invalid file_agent action: {action}"
        try:
            return getattr(self, action)(**args)
        except Exception as e:
            return f"Execution error: {str(e)}"

    # FILE OPERATIONS

    def create_file(self, path=None, filename=None):
        full_path = self._resolve_full_path(path, filename)
        if os.path.exists(full_path):
            return f"File already exists at {full_path} (skipped)"

        open(full_path, "w").close()
        return f"File created at {full_path}"

    def write_file(self, path=None, filename=None, content=""):
        full_path = self._resolve_full_path(path, filename)
        with open(full_path, "w") as f:
            f.write(content)
        
        return f"File written at {full_path}"

    def read_file(self, path=None, filename=None):
        full_path = self._resolve_full_path(path, filename)
        if not os.path.exists(full_path):
            return "File does not exist"

        with open(full_path, "r") as f:
            return f.read()

    def delete_file(self, path=None, filename=None):
        full_path = self._resolve_full_path(path, filename)
        if os.path.exists(full_path):
            os.remove(full_path)
            return "File deleted"

        return "File not found"

    def list_files(self):
        result = {}

        for folder in ["documents", "codes", "data", "databases"]:
            dir_path = os.path.join(BASE_DIR, folder)
            os.makedirs(dir_path, exist_ok=True)
            result[folder] = os.listdir(dir_path)

        return result