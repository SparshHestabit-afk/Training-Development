import os
import io
import re
import traceback
import contextlib

BASE_DIR = "src/files"

class CodeAgent:

    # PATH RESOLUTION
    def _safe_path(self, filename):
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

    # CODE PREPROCESSING (CORE FIX)
    def _sanitize_code(self, code):
        """
        Force all file access into src/files/
        Prevent LLM from using ~/Documents or custom paths
        """

        # remove home directory usage
        code = code.replace("os.path.expanduser('~')", f"'{BASE_DIR}'")
        code = code.replace('os.path.expanduser(\"~\")', f"'{BASE_DIR}'")

        # normalize Documents → data
        code = code.replace("Documents", "data")

        # fix read_csv("file.csv")
        matches = re.findall(r"read_csv\(['\"](.*?)['\"]\)", code)

        for file in matches:
            safe = self._safe_path(file)
            code = code.replace(file, safe)

        # fix to_csv("file.csv")
        matches = re.findall(r"to_csv\(['\"](.*?)['\"]", code)

        for file in matches:
            filename = os.path.basename(file)
            safe_path = self._safe_path(filename)
            code = code.replace(file, safe_path)

        return code

    # EXECUTION
    def _run(self, code):
        try:
            local_vars = {}
            buffer = io.StringIO()

            def safe_open(file, mode="r", *args, **kwargs):
                return open(self._safe_path(file), mode, *args, **kwargs)

            safe_globals = {
                "__builtins__": __builtins__,
                "open": safe_open
            }

            # enforce path safety
            code = self._sanitize_code(code)

            print("\n[EXECUTING CODE]")
            print(code)

            with contextlib.redirect_stdout(buffer):
                exec(code, safe_globals, local_vars)

            output = buffer.getvalue().strip()
            
            return {
                "success": True,
                "output": output if output else "Execution completed (no output)",
                "has_output": bool(output)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    # RETRY LOOP
    def _execute_with_retry(self, code, client, model, max_attempts=3):
        attempt = 0

        while attempt < max_attempts:
            result = self._run(code)

            if result["success"]:
                return result
            
            # Only retry on real execution errors
            if "syntax" not in result.get("error", "").lower() and \
                "name" not in result.get("error", "").lower():
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

            code = self._clean(response.choices[0].message.content)
            attempt += 1

        return {
            "success": False,
            "error": "Max retry attempts reached",
            "last_code": code
        }

    # CLEAN CODE
    def _clean(self, code):
        return "\n".join(
            line for line in code.split("\n")
            if not line.strip().startswith("```")
        )

    # MAIN ENTRY
    def handle_task(self, step, query, client, model):
        args = step.get("args", {})

        # DIRECT CODE EXECUTION
        if "code" in args:
            return self._execute_with_retry(args["code"], client, model)

        # TASK → GENERATE CODE
        if "task" in args:
            prompt = f"""
                Write Python code for:
                {args["task"]}

                Rules:
                - Use pandas for CSV
                - No explanations
                - Code must run
            """
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            code = self._clean(response.choices[0].message.content)
            return self._execute_with_retry(code, client, model)

        return {"success": False, "error": "Invalid input"}