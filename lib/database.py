from lib.db.connection import get_connection
from pathlib import Path

def initialize_database():
    schema_path = Path(__file__).parent / "db" / "schema.sql"
    with get_connection() as conn:
        with open(schema_path, "r") as file:
            schema_sql = file.read()
            conn.executescript(schema_sql)
            print("✅ Schema applied successfully.")

if __name__ == "__main__":
    initialize_database()
