import os
import yaml
from groq import Groq

class SQLGenerator:

    def __init__(self, model_config_path="src/config/model.yaml"):

        with open(model_config_path, "r") as f:
            config = yaml.safe_load(f)

        api_key = os.getenv(config["api_key_env"])
        self.model_name = config["model_name"]

        if not api_key:
            raise ValueError(
                f"Environment variable {config['api_key_env']} not set"
            )

        self.client = Groq(api_key=api_key)

    # ---------------------------------
    # Clean SQL output
    # ---------------------------------

    def _clean_sql(self, text: str) -> str:

        sql = text.strip()

        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")

        return sql.strip()

    # ---------------------------------
    # Internal LLM call
    # ---------------------------------

    def _ask_llm(self, prompt: str) -> str:

        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        return completion.choices[0].message.content

    # ---------------------------------
    # SQL Generation
    # ---------------------------------

    def generate_sql(self, question: str, schema: str) -> str:

        prompt = f"""
You are a PostgreSQL expert.

Database Schema:
{schema}

Convert the user question into SQL.

Rules:
- Use only tables and columns in schema
- Only SELECT queries
- PostgreSQL syntax
- Return SQL only
- No explanations

User Question:
{question}
"""

        response = self._ask_llm(prompt)

        return self._clean_sql(response)

    # ---------------------------------
    # Error Correction
    # ---------------------------------

    def correct_sql(self, question: str, schema: str, sql: str, error: str) -> str:

        prompt = f"""
The following SQL query failed.

Database Schema:
{schema}

User Question:
{question}

SQL Query:
{sql}

Error:
{error}

Fix the SQL query.

Rules:
- Only SELECT queries
- PostgreSQL syntax
- Return only SQL
"""

        response = self._ask_llm(prompt)

        return self._clean_sql(response)

    # ---------------------------------
    # Result Summarization
    # ---------------------------------

    def summarize(self, question: str, table: str) -> str:

        prompt = f"""
User Question:
{question}

SQL Result Table:
{table}

Explain the result clearly in natural language.
"""

        response = self._ask_llm(prompt)

        return response.strip()