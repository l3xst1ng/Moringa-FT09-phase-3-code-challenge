from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category (optional): ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create an author
    author = Author(None, author_name)
    author.create(cursor)

    # Create a magazine
    magazine = Magazine(None, magazine_name, magazine_category)
    magazine.create(cursor)

    # Create an article
    article = Article.create_article(cursor, article_title, article_content, author.id, magazine.id)

    conn.commit()

    # Query the database for inserted records
    magazines = Magazine.get_all(cursor)
    authors = Author.get_all(cursor)
    article_titles = Article.get_titles(cursor)

    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(magazine)

    print("\nAuthors:")
    for author in authors:
        print(author)

    print("\nArticle Titles:")
    print(article_titles)

    print("\nCreated Article:")
    print(article)
    print("Author of the article:", article.get_author(cursor))
    print("Magazine of the article:", article.get_magazine(cursor))

if __name__ == "__main__":
    main()