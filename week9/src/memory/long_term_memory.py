import sqlite3
import os

BASE_DIR = "src/memory"
DB_PATH = os.path.join(BASE_DIR, "long_term.db")

class LongTermMemory:

    def __init__(self):
        os.makedirs(BASE_DIR, exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH) #establishing the connection to the .db file, for later operations
        # it make our databse act like dictionary, allowing to access columns by name rather than id, making it easy to maintain
        self.conn.row_factory = sqlite3.Row # formatting the response from the table , to make it easy to understnad,
        self._create_table() # creates a table for memory for persistant storage, with two fields, id & content

    # INIT TABLE (memory table for storage)
    def _create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
        """)
        self.conn.commit() # coomiting the execution, so that table can be created if it doesn't exist

    # ADD MEMORY ( adding values or records to the table, which are actually the chats)
    def add(self, content):
        if not content or len(str(content).strip()) == 0: # skip empty, null or whitespace entries to maintain the quality of memory
            return

        self.conn.execute( # adding the content to the memory table 
            "INSERT INTO memory (content) VALUES (?)", # uses placeholder value, to prevent SQL injection, (as llm can generate wrong or invalid input)
            (str(content),)
        )
        self.conn.commit()

    # GET RECENT MEMORY (short term recall)
    def get_recent(self, limit=None):
        cursor = self.conn.cursor() # creating a cursor object, which is used to execute sql commands
        cursor.execute(
            "SELECT content FROM memory ORDER BY id DESC LIMIT ?",
            (limit,) # limit is defining the size of memory window to be retrieved, done for limiting (no. of records and token control)
        )
        rows = cursor.fetchall() # retrieves or fetches all the matching rows in the database, and loads into a row object
        return [row["content"] for row in rows] # tranforms database rows into a list of string

    # USER PROFILE (PERSONALIZATION) (used for giving content to the llm, to make it understand the user better, and personalize the response based on the user profile)
    def get_user_profile(self, limit=None):
        recent = self.get_recent(limit)
        return "\n".join(recent)

    # UPDATING CONTEXT ( used for updating the context, based on the relevance of the memory, for the final system prompt, which include memory recall)
    def update_context(self, messages, query):
        long_memories = self.get_recent(limit=5)
        user_profile = self.get_user_profile(limit=10)
        combined = []

        if user_profile:
            combined.append(f"User Profile:\n{user_profile}")
        if long_memories:
            combined.append("Recent Long-Term Memory:\n" + "\n".join(long_memories))
        if not combined:
            return messages # not modifying the context, or input message

        memory_message = { # creating a strucured message for the memory, to make it llm ready (system message/instruction)
            "role": "system",
            "content": "\n\n".join(combined)
        }
        return messages[:-1] + [memory_message] + [messages[-1]] # 'list sandwitch', where we ensure that llm reads the memory once, befoore generating any new response

    # COUNT MEMORY (a basic quick healthcheck, and as well as memory statistics, and counter(counting number of chat stored) ) 
    def count(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM memory")
        result = cursor.fetchone()

        return result["total"] if result else 0

    # CLEAR MEMORY (to clean and restart the memory)
    def clear(self):
        self.conn.execute("DELETE FROM memory")
        self.conn.commit()