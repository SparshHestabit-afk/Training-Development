import sqlite3
import os

BASE_DIR = "src/files"
class DBAgent:

    SYSTEM_PROMPT = """
        You are db_agent.

        ROLE:
        SQLite database execution engine.

        CAPABILITIES:
        - execute ANY SQL query
        - create tables
        - insert data
        - update records
        - delete records
        - select data
        - alter tables
        - drop tables

        RULES:
        1. Always ensure connection exists
        2. SQL must be valid
        3. Commit changes when needed
        4. Never assume schema

        BEHAVIOR:
        - deterministic
        - strict SQL execution
    """

    def __init__(self):
        self.conn = None
        self.current_db = None

    #  PATH RESOLLUTION
    def _resolve_db_path(self, db_name=None):
        if not db_name:
            db_name = "database.db"

        db_name = os.path.basename(db_name)
        full_path = os.path.join(BASE_DIR, "databases", db_name)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        return full_path
    
    # CONNECTION (FINAL)
    def connect(self, db_name = None):
        db_path = self._resolve_db_path(db_name)
        # Reconnect if db closes or db changes
        if self.conn is None or self.current_db != db_path:
            if self.conn:
                self.conn.close()

            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = sqlite3.Row
            self.current_db = db_path

    # SQL CLEANING
    def _clean_sql(self, query):

        query = query.strip()
        query = query.replace("```sql", "")
        query = query.replace("```", "")

        return query.strip()
    
    # MAIN ENTRY
    def handle_task(self, step, query, client, model):

        args = step.get("args", {})
        action = step.get("action")

        if action != "execute_sql":
            return {
                "success": False,
                "error": f"Invalid action: {action}"
            }

        sql_query = args.get("query")
        db_name = args.get("db_name")  # optional

        if not sql_query:
            return {
                "success": False,
                "error": "Missing SQL query"
            }
        
        self.connect(db_name)
        return self.execute_sql(sql_query)

    # SQL EXECUTION (FINAL)
    def execute_sql(self, query):

        try:
            query = self._clean_sql(query)
            cursor = self.conn.cursor()
            # Support multiple SQL statements
            statements = [
                q.strip() for q in query.split(";") if q.strip()
            ]
            
            last_result = None
            for stmt in statements:
                cursor.execute(stmt)
                stmt_lower = stmt.lower()

                # SELECT queries
                if stmt_lower.startswith(("select", "pragma", "with")):
                    rows = cursor.fetchall()
                    last_result = [dict(row) for row in rows]

                # Other queries ( UPDATE OR DELETE, command that changes' database state, mainly)
                else:
                    self.conn.commit()
                    last_result = {"message": "Command executed"}

            return {
                "success": True,
                "result": last_result,
                "rows": len(last_result) if isinstance(last_result, list) else None
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }