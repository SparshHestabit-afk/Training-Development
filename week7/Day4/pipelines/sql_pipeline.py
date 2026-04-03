import re
import psycopg2
import pandas as pd

from src.generator.sql_generator import SQLGenerator
from src.utils.schema_loader import SchemaLoader


class SQLPipeline:

    def __init__(self, db_config):

        print("\nInitializing SQL QA Pipeline")

        self.db_config = db_config

        # ---------------------------------------
        # Load Schema
        # ---------------------------------------

        loader = SchemaLoader(db_config)

        schema_dict = loader.load_schema()
        self.schema = loader.format_schema_for_prompt(schema_dict)

        print("\nDatabase Schema Loaded:")
        print(self.schema)

        # ---------------------------------------
        # LLM Generator
        # ---------------------------------------

        self.generator = SQLGenerator()

    # ---------------------------------------
    # Query Validation
    # ---------------------------------------

    def _validate_sql(self, sql: str):

        forbidden = [
            "DROP",
            "DELETE",
            "INSERT",
            "UPDATE",
            "ALTER",
            "TRUNCATE"
        ]

        sql_upper = sql.upper()

        if not sql_upper.startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")

        for keyword in forbidden:
            if keyword in sql_upper:
                raise ValueError(
                    f"Dangerous SQL keyword detected: {keyword}"
                )

        if re.search(r";\s*DROP", sql_upper):
            raise ValueError("Possible SQL injection detected")

        return True

    # ---------------------------------------
    # Safe SQL Execution
    # ---------------------------------------

    def _execute_sql(self, sql: str) -> pd.DataFrame:

        try:

            conn = psycopg2.connect(**self.db_config)

            df = pd.read_sql_query(sql, conn)

            conn.close()

            return df

        except Exception as e:

            raise RuntimeError(str(e))

    # ---------------------------------------
    # Main Pipeline
    # ---------------------------------------

    def run(self, question: str):

        print("\nUser Question:", question)

        sql = self.generator.generate_sql(question, self.schema)

        retries = 0
        max_retries = 2

        while retries <= max_retries:

            try:

                print("\nGenerated SQL:")
                print(sql)

                # Query validation
                self._validate_sql(sql)

                # Safe execution
                result = self._execute_sql(sql)

                print("\nQuery Result:")
                print(result)

                # Summarize results
                summary = self.generator.summarize(
                    question,
                    result.to_string()
                )

                print("\nFinal Answer:")
                print(summary)

                return {
                    "sql": sql,
                    "result": result,
                    "summary": summary
                }

            except Exception as e:

                print("\nSQL Error:", e)

                # Error correction
                sql = self.generator.correct_sql(
                    question,
                    self.schema,
                    sql,
                    str(e)
                )

                retries += 1

        raise RuntimeError("SQL generation failed after retries")

# ---------------------------------------
# Quick Debug Runner
# ---------------------------------------

if __name__ == "__main__":

    db_config = {
        "host": "localhost",
        "port": 5432,
        "database": "music_db",
        "user": "postgres",
        "password": "postgres"
    }

    pipeline = SQLPipeline(db_config)

    print("\nSQL QA System Ready\n")

    while True:

        question = input("Ask a SQL question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        try:

            result = pipeline.run(question)

            print("\nSummary:")
            print(result["summary"])

        except Exception as e:

            print("\nPipeline Error:", e)