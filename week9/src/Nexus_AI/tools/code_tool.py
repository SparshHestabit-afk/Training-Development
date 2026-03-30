import subprocess
import os
import sys
import datetime

from config import WORKSPACE_DIR

class CodeTool:

    def __init__(self, timeout=10):
        self.timeout = timeout
        self.workspace = WORKSPACE_DIR
        os.makedirs(self.workspace, exist_ok=True)

    def run(self, code: str):
        """
        Execute Python code inside workspace.
        Any files created will be stored in workspace.
        """

        if not code or not code.strip():
            return "No code provided."

        # Basic safety filter
        blocked_keywords = [
            "os.system",
            "subprocess",
            "rm -rf",
            "__import__",
            "eval",
            "exec"
        ]

        for keyword in blocked_keywords:
            if keyword in code:
                return f"Blocked unsafe operation: {keyword}"

        try:
            # Create unique file for saved code
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            code_filename = f"generated_code_{timestamp}.py"
            code_path = os.path.join(self.workspace, code_filename)

            # Save the code file
            with open("output.py", "w") as f:
                f.write(code)

            # Execute inside workspace
            result = subprocess.run(
                [sys.executable, code_path],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.workspace  
            )

            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            if stderr:
                return f"ERROR:\n{stderr}"
            elif stdout:
                response += f"\n OUTPUT:\n{stdout}"
            else:
                response += "\n Code executed successfully (no output)."

        except subprocess.TimeoutExpired:
            return "Execution timed out."

        except Exception as e:
            return f"Execution failed: {str(e)}"