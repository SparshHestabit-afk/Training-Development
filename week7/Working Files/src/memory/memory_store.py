import json
import os
from datetime import datetime


class MemoryStore:

    def __init__(self, file_path="src/logs/CHAT-LOGS.json", max_memory=5):

        self.file_path = file_path
        self.max_memory = max_memory

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump([], f)

    def load_memory(self):

        if not os.path.exists(self.file_path):
            return []

        if os.path.getsize(self.file_path) == 0:
            return []
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return []

        return data[-self.max_memory:]

    def format_memory(self):

        memory = self.load_memory()

        formatted = ""

        for m in memory:
            formatted += f"User: {m['question']}\n"
            formatted += f"Assistant: {m['answer']}\n\n"

        return formatted

    def save_interaction(self, question, answer, confidence, trace=None):

        with open(self.file_path, "r") as f:
            logs = json.load(f)

        logs.append({
            "timestamp": str(datetime.now()),
            "question": question,
            "answer": answer,
            "confidence": confidence,
            "trace": trace or {}
        })

        with open(self.file_path, "w") as f:
            json.dump(logs, f, indent=2)

    def save_feedback(self, question, answer, feedback):

        entry = {
            "question": question,
            "answer": answer,
            "feedback": feedback
        }
        data = []

        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    data = json.load(f)
                except:
                    data = []

        data.append(entry)
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)