import subprocess
import os
import io
import sys
import traceback
import contextlib

BASE_DIR = "src/files"

class CodeAgent:

    SYSTEM_PROMPT = """
        You are code_agent.
        ROLE:
        Python code generator, executor, and debugger.
        RULES:
        1. Return ONLY Python code
        2. No explanation, no markdown
        3. Code must be executable
        4. Fix errors if any
    """

    # PATH HANDLING (FINAL)
    def _safe_write_path(self, filename):

        filename = os.path.basename(filename)

        if filename.endswith(".csv"):
            folder = "data"
        elif filename.endswith(".db"):
            folder = "databases"
        elif filename.endswith(".txt"):
            folder = "documents"
        else:
            folder = "codes"

        full_path = os.path.join(BASE_DIR, folder, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        return full_path

    # MAIN ENTRY
    def handle_task(self, step, query, client, model):
        args = step.get("args", {})

    # NORMALIZE INPUT KEYS (FINAL FIX)
        filename = (
            args.get("filename")
            or args.get("file")
            or args.get("input_file")
            or args.get("path")
        )

        output_file = args.get("output_file")
        task = args.get("task", "").lower()
        task = args.get("task", "").lower()

        # CSV CREATE / APPEND
        if "filename" in args and "data" in args:
            import pandas as pd
            import os

            filename = args["filename"]
            data = args["data"]

            full_path = self._safe_write_path(filename)

            # list-of-lists format
            if isinstance(data, list):
                df = pd.DataFrame(data[1:], columns=data[0])

            # dict format
            elif isinstance(data, dict):
                df = pd.DataFrame(data)

            else:
                return {"success": False, "error": "Unsupported data format"}

            # append mode
            if "append" in task and os.path.exists(full_path):

                existing_df = pd.read_csv(full_path)
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                combined_df.to_csv(full_path, index=False)

                return {
                    "success": True,
                    "message": f"Data appended to {full_path}"
                }

            # create mode
            else:
                df.to_csv(full_path, index=False)

                return {
                    "success": True,
                    "message": f"CSV created at {full_path}"
                }

        # CSV → DB
        if "convert_csv_to_db" in task:

            import pandas as pd
            import sqlite3
            import os

            if not filename:
                return {"success": False, "error": "Missing filename"}

            csv_path = self._safe_write_path(filename)
            if not os.path.exists(csv_path):
                return {"success": False, "error": f"CSV not found: {csv_path}"}

            db_name = output_file or filename.replace(".csv", ".db")
            db_path = self._safe_write_path(db_name)
            df = pd.read_csv(csv_path)

            conn = sqlite3.connect(db_path)
            table_name = filename.replace(".csv", "")
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            conn.close()

            return {
                "success": True,
                "message": f"Database created at {db_path}",
                "table": table_name
            }

        # DB ANALYSIS
        if "analyse" in task or "analyze" in task:

            import sqlite3
            import os

            if not filename:
                return {"success": False, "error": "Missing filename"}

            # allow .db or .csv input
            if filename.endswith(".csv"):
                db_name = filename.replace(".csv", ".db")
            else:
                db_name = filename

            db_path = self._safe_write_path(db_name)

            if not os.path.exists(db_path):
                return {"success": False, "error": f"DB not found: {db_path}"}

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            table_name = db_name.replace(".db", "")

            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]

                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                rows = cursor.fetchall()

                conn.close()

                return {
                    "success": True,
                    "analysis": {
                        "table": table_name,
                        "total_rows": count,
                        "sample_data": rows
                    }
                }

            except Exception as e:
                return {"success": False, "error": str(e)}

        # GENERIC CODE EXECUTION
        if "code" in args:
            return self.execute_with_retry(args["code"], client, model, query)

        if "task" in args:
            return self.generate_and_execute(args["task"], client, model)

        file_path = args.get("filename") or args.get("path")

        if file_path:
            try:
                filename = os.path.basename(file_path)
                full_path = os.path.join(BASE_DIR, "codes", filename)

                if not os.path.exists(full_path):
                    return {"success": False, "error": f"File not found: {full_path}"}

                with open(full_path, "r") as f:
                    code = f.read()

                return self.execute_with_retry(code, client, model, query)

            except Exception as e:
                return {"success": False, "error": str(e)}

        return {"success": False, "error": "Invalid code_agent input"}

    # GENERATE + RUN
    def generate_and_execute(self, task, client, model):
        prompt = f"""
            Write Python code for:
            {task}

            Rules:
            - Save files using safe paths
            - Use pandas for CSV
            - Use sqlite3 for DB
            - No explanations
        """
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        code = self.clean_code(response.choices[0].message.content)
        return self.execute_with_retry(code, client, model, task)

    # RETRY LOOP
    def execute_with_retry(self, code, client, model, query, max_attempts=3):

        attempt = 0
        while attempt < max_attempts:
            code = self.clean_code(code)
            result = self.run_python(code)

            if result["success"]:
                return result
            fix_prompt = f"""
                Fix this Python code:
                {code}
                
                Error:
                {result["error"]}
                
                Return ONLY corrected Python code.
            """
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": fix_prompt}],
                temperature=0
            )
            code = self.clean_code(response.choices[0].message.content)
            attempt += 1

        return {
            "success": False,
            "error": "Max retry attempts reached",
            "last_code": code
        }

    # EXECUTION
    def run_python(self, code):
        try:
            local_vars = {}
            output_buffer = io.StringIO()

            # Safe file path override
            def safe_open(filename, mode="r", *args, **kwargs):
                safe_path = self._safe_write_path(filename)
                return open(safe_path, mode, *args, **kwargs)

            safe_globals = {
                "__builtins__": __builtins__,
                "open": safe_open
            }

            with contextlib.redirect_stdout(output_buffer):
                exec(code, safe_globals, local_vars)
            printed_output = output_buffer.getvalue().strip()
            return {
                "success": True,
                "output": printed_output if printed_output else "Execution Completed"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    # CLEAN CODE
    def clean_code(self, code):
        return "\n".join([
            line for line in code.split("\n")
            if not line.strip().startswith("```")
        ])