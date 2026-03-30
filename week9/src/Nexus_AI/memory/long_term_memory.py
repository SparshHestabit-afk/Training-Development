import sqlite3
import os

class LongTermMemory:

    def __init__(self):
        # Path to the directory , where we are storing our memory
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        MEMORY_DIR = os.path.join(BASE_DIR, "memory_store")
        os.makedirs(MEMORY_DIR, exist_ok=True)

        self.db_path = os.path.join(MEMORY_DIR, "nexus_long_term.db")
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    # Initializing and Creating Table 
    def _create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
        """)
        self.conn.commit()

    # ADD MEMORY
    def add(self, content):
        if not content or len(str(content).strip()) == 0:
            return

        self.conn.execute(
            "INSERT INTO memory (content) VALUES (?)",
            (str(content),)
        )
        self.conn.commit()

    # GET RECENT MEMORY
    def get_recent(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT content FROM memory ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        return [row["content"] for row in rows]
    
    # USER PROFILE (PERSONALIZATION)
    def get_user_profile(self, limit=5):
        recent = self.get_recent(limit)
        return "\n".join(recent)
    
    # UPDATING CONTEXT
    def update_context(self, messages, query):
        long_memories = self.get_recent()
        user_profile = self.get_user_profile()
        combined = []

        if user_profile:
            combined.append(f"User Profile:\n{user_profile}")
        if long_memories:
            combined.append("Recent Long-Term Memory:\n" + "\n".join(long_memories))
        if not combined:
            return messages

        memory_message = {
            "role": "system",
            "content": "\n\n".join(combined)
        }
        return messages[:-1] + [memory_message] + [messages[-1]]
    
    # COUNT MEMORY
    def count(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM memory")
        result = cursor.fetchone()
        return result["total"] if result else 0
    
    # CLEAR MEMORY
    def clear(self):
        self.conn.execute("DELETE FROM memory")
        self.conn.commit()