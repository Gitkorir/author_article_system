from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
import random

def seed_database():
    """Populate the database with sample data"""
    print(" Seeding database...")
    
    # Clear existing data
    with get_connection() as conn:
        conn.execute("DELETE FROM articles")
        conn.execute("DELETE FROM authors")
        conn.execute("DELETE FROM magazines")
        conn.commit()

    # Sample data
    authors = [
       Author(name="Alice", email="alice@example.com"),
       Author(name="John Doe", email="john@example.com"),
       Author(name="Jane Smith", email="jane@example.com"),
       Author(name="Mike Johnson", email="mike@example.com"),
       Author(name="Sarah Williams", email="sarah@example.com")
]
    magazines = [
       Magazine(name="Tech Today", category="Technology"),
       Magazine(name="Science Weekly", category="Science"),
       Magazine(name="Business Insights", category="Business"),
       Magazine(name="Creative Minds", category="Arts")
]

   

    articles_data = [
        {"title": "The Future of AI", "content": "Lorem ipsum..."},
        {"title": "Quantum Computing", "content": "Lorem ipsum..."},
        {"title": "Market Trends 2023", "content": "Lorem ipsum..."},
        {"title": "Modern Art Movements", "content": "Lorem ipsum..."},
        {"title": "Python Programming", "content": "Lorem ipsum..."},
        {"title": "Renewable Energy", "content": "Lorem ipsum..."},
        {"title": "Startup Funding", "content": "Lorem ipsum..."},
        {"title": "Digital Painting", "content": "Lorem ipsum..."}
    ]

    # Save authors and magazines
    for author in authors:
        author.save()
    
    for magazine in magazines:
        magazine.save()

    # Create articles with random assignments
    for article_data in articles_data:
        author = random.choice(authors)
        magazine = random.choice(magazines)
        Article(
            title=article_data["title"],
            content=article_data["content"],
            author_id=author.id,
            magazine_id=magazine.id
        ).save()

    print(" Database seeded successfully!")
    print(f"Created: {len(authors)} authors, {len(magazines)} magazines, {len(articles_data)} articles")

if __name__ == "__main__":
    seed_database()