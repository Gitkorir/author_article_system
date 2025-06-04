from lib.db.connection import get_connection

def test_database():
    print("✅ Connecting to the database...")
    with get_connection() as conn:
        print("✅ Connection successful.")

        # Read schema and create tables
        with open("lib/db/schema.sql", "r") as schema_file:
            schema_sql = schema_file.read()
        conn.executescript(schema_sql)
        print("✅ Tables created.")

        # Insert sample data
        conn.execute(
    "INSERT INTO authors (name, bio, email) VALUES (?, ?, ?)",
    ("Arnold", "Software Engineering Student", "arnold@example.com")
)

        conn.commit()
        print("✅ Sample data inserted.")

        # Query and print data
        cursor = conn.execute("""
           SELECT authors.name, articles.title
           FROM authors
           JOIN articles ON authors.id = articles.author_id
""")
        for row in cursor:
         print(f"👤 Author: {row['name']} | 📝 Article: {row['title']}")

if __name__ == "__main__":
    test_database()
