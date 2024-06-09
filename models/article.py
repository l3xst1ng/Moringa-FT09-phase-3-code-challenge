class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        """
        Initializes an Article instance.

        Args:
            id (int): The ID of the article.
            title (str): The title of the article.
            content (str): The content of the article.
            author_id (int): The ID of the author associated with the article.
            magazine_id (int): The ID of the magazine associated with the article.
        """
        self._id = id
        self.title = title
        self.content = content
        self._author_id = author_id
        self._magazine_id = magazine_id



    @property
    def id(self):
        """
        Gets the ID of the article.

        Returns:
            int: The ID of the article.
        """
        return self._id



    @property
    def title(self):
        """
        Gets the title of the article.

        Returns:
            str: The title of the article.
        """
        return self._title
    
    

    @title.setter
    def title(self, value):
        """
        Sets the title of the article.

        Args:
            value (str): The title of the article.

        Raises:
            ValueError: If the title is not a string or not between 5 and 50 characters.
        """
        if isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value
        else:
            raise ValueError("Title must be a string between 5 and 50 characters")



    @classmethod
    def create_article(cls, cursor, title, content, author_id, magazine_id):
        """
        Creates a new article in the database.

        Args:
            cursor: The database cursor.
            title (str): The title of the article.
            content (str): The content of the article.
            author_id (int): The ID of the author associated with the article.
            magazine_id (int): The ID of the magazine associated with the article.

        Returns:
            Article: The created Article instance.
        """
        cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
            (title, content, author_id, magazine_id))
        article_id = cursor.lastrowid
        return cls(article_id, title, content, author_id, magazine_id)



    @classmethod
    def get_titles(cls, cursor):
        """
        Gets all article titles from the database.

        Args:
            cursor: The database cursor.

        Returns:
            list: A list of article titles, or None if no titles are found.
        """
        cursor.execute("SELECT title FROM articles")
        titles = cursor.fetchall()
        return [title[0] for title in titles] if titles else None



    def get_author(self, cursor):
        """
        Gets the name of the author associated with the article.

        Args:
            cursor: The database cursor.

        Returns:
            str: The name of the author, or None if not found.
        """
        cursor.execute("SELECT name FROM authors WHERE id = ?", (self._author_id,))
        author_name = cursor.fetchone()
        return author_name[0] if author_name else None



    def get_magazine(self, cursor):
        """
        Gets the name of the magazine associated with the article.

        Args:
            cursor: The database cursor.

        Returns:
            str: The name of the magazine, or None if not found.
        """
        cursor.execute("SELECT name FROM magazines WHERE id = ?", (self._magazine_id,))
        magazine_name = cursor.fetchone()
        return magazine_name[0] if magazine_name else None