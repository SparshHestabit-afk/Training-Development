import os
import csv

from config import WORKSPACE_DIR

class FileTool:

    def __init__(self):
        self.base_dir = WORKSPACE_DIR
        os.makedirs(self.base_dir, exist_ok=True)

    # LIST FILES
    def list_files(self):
        try:
            files = os.listdir(self.base_dir)
            return files if files else "No files found."
        except Exception as e:
            return f"Error listing files: {str(e)}"

    # READ FILE
    def read(self, filename):
        file_path = os.path.join(self.base_dir, filename)

        if not os.path.exists(file_path):
            return f"File not found: {filename}"

        try:
            with open(file_path, "r") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    # SAVE FILE (CREATE / OVERWRITE)
    def save_file(self, filename, content):
        """
        Create or overwrite a file.
        """
        file_path = os.path.join(self.base_dir, filename)

        try:
            with open(file_path, "w") as f:
                f.write(content)
            return f"File saved: {filename}"
        except Exception as e:
            return f"Error saving file: {str(e)}"

    # APPEND FILE (UPDATE)
    def append_file(self, filename, content):
        """
        Append content to a file.
        """
        file_path = os.path.join(self.base_dir, filename)

        try:
            with open(file_path, "a") as f:
                f.write("\n" + content)
            return f"Content appended to: {filename}"
        except Exception as e:
            return f"Error appending file: {str(e)}"

    # DELETE FILE
    def delete(self, filename):
        file_path = os.path.join(self.base_dir, filename)

        if not os.path.exists(file_path):
            return f"File not found: {filename}"

        try:
            os.remove(file_path)
            return f"File deleted: {filename}"
        except Exception as e:
            return f"Error deleting file: {str(e)}"

    # READ CSV
    def read_csv(self, filename, limit=10):
        file_path = os.path.join(self.base_dir, filename)

        if not os.path.exists(file_path):
            return f"CSV not found: {filename}"

        try:
            with open(file_path, newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)[:limit]

            return rows if rows else "CSV is empty."
        except Exception as e:
            return f"Error reading CSV: {str(e)}"

    # WRITE CSV
    def write_csv(self, filename, data):
        file_path = os.path.join(self.base_dir, filename)

        try:
            if not isinstance(data, list) or not data:
                return "Invalid CSV data format."

            keys = data[0].keys()

            with open(file_path, "w", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)

            return f"CSV saved: {filename}"
        except Exception as e:
            return f"Error writing CSV: {str(e)}"