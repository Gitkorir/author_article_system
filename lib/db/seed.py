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
        Author("John Doe", "john@example.com"),
        Author("Jane Smith", "jane@example.com"),
        Author("Mike Johnson", "mike@example.com"),
        Author("Sarah Williams", "sarah@example.com")
    ]

    magazines = [
        Magazine("Tech Today", "Technology"),
        Magazine("Science Weekly", "Science"),
        Magazine("Business Insights", "Business"),
        Magazine("Creative Minds", "Arts")
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