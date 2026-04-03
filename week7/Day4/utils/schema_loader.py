import psycopg2
from typing import Dict, List

class SchemaLoader:

    def __init__(self, db_config: Dict):

        self.db_config = db_config

    # ----------------------------------
    # Load Schema From PostgreSQL
    # ----------------------------------

    def load_schema(self) -> Dict[str, List[Dict]]:

        schema = {}

        try:

            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()

            query = """
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                ORDER BY table_name, ordinal_position;
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                raise RuntimeError("No tables found in database")

            for table_name, column_name, data_type in rows:

                if table_name not in schema:
                    schema[table_name] = []

                schema[table_name].append({
                    "column": column_name,
                    "type": data_type
                })

            cursor.close()
            conn.close()

        except Exception as e:
            raise RuntimeError(f"[SchemaLoader Error] {e}")

        return schema

    # ----------------------------------
    # Convert Schema → Prompt Format
    # ----------------------------------

    def format_schema_for_prompt(self, schema: Dict) -> str:

        schema_text = ""

        for table, columns in schema.items():
            schema_text += f"\nTable: {table}\n"

            for col in columns:
                schema_text += f"  - {col['column']} ({col['type']})\n"

        return schema_text