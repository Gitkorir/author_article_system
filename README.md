# author_article_system

A Python application modeling relationships between authors, articles, and magazines with SQLite persistence.

## Features

- **Model Relationships**:
  - Authors write many Articles
  - Magazines publish many Articles
  - Many-to-many Author-Magazine relationships
- **Database Operations**:
  - CRUD operations for all entities
  - Complex SQL queries with joins
  - Transaction management
- **Validation**:
  - Data integrity checks
  - Custom validation rules
- **Developer Tools**:
  - Interactive debug console
  - Database seeding script

## Project Structure
code-challenge/
├── lib/ # Main application code
│ ├── models/ # Database models
│ ├── db/ # Database components
│ ├── controllers/ # Business logic
│ └── debug.py # Interactive console
├── tests/ # Unit tests
├── scripts/ # Utility scripts
├── data/ # Database files
└── README.md # Project documentation


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/magazine-article-system.git
   cd magazine-article-system

2. Setting up a vitual env  
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate  # Windows

3. initialize the db
     python scripts/setup_db.py
     python -m lib.db.seed 


   Usage
Running the Application
bash
   python main.py
Interactive Debug Console
bash
   python -m lib.debug  


## Key Methods
>Author
articles() - Get all articles by author

magazines() - Get all magazines author contributed to

add_article(magazine, title, content) - Create new article

top_writers() - Get most prolific authors

>Magazine
articles() - Get all magazine articles

contributors() - Get all contributing authors

article_titles() - List all article titles

most_popular() - Get top magazines by article count

>Article
author() - Get article's author

magazine() - Get publishing magazine

search(query) - Full-text search

recent() - Get latest articles


