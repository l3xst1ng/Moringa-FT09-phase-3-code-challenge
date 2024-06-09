class Author:
    def __init__(self, id, name):
        """
        Initializes an Author instance.

        Args:
            id (int): The ID of the author.
            name (str): The name of the author.
        """
        self._id = id
        self._name = name



    @property
    def id(self):
        """
        Gets the ID of the author.

        Returns:
            int: The ID of the author.
        """
        return self._id



    @property
    def name(self):
        """
        Gets the name of the author.

        Returns:
            str: The name of the author.
        """
        return self._name



    @name.setter
    def name(self, value):
        """
        Sets the name of the author.

        Args:
            value (str): The name of the author.

        Raises:
            TypeError: If the name is not a string.
            ValueError: If the name is empty.
            AttributeError: If the name is being changed after instantiation.
        """
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if len(value) == 0:
            raise ValueError("Name must not be empty.")
        if hasattr(self, '_name'):
            raise AttributeError("Name cannot be changed after instantiation.")
        self._name = value



    def create(self, cursor):
        """
        Creates a new author in the database.

        Args:
            cursor: The database cursor.
        """
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
        self._id = cursor.lastrowid



    @classmethod
    def get_all(cls, cursor):
        """
        Gets all authors from the database.

        Args:
            cursor: The database cursor.

        Returns:
            list: A list of Author instances.
        """
        cursor.execute("SELECT * FROM authors")
        authors_data = cursor.fetchall()
        return [cls(id=row[0], name=row[1]) for row in authors_data]



    def get_articles(self, cursor):
        """
        Gets all articles associated with the author from the database.

        Args:
            cursor: The database cursor.

        Returns:
            list: A list of article data tuples.
        """
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        articles_data = cursor.fetchall()
        return articles_data



    def get_magazines(self, cursor):
        """
        Gets all magazines associated with the author from the database.

        Args:
            cursor: The database cursor.

        Returns:
            list: A list of magazine data tuples.
        """
        cursor.execute("""
            SELECT magazines.*
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self._id,))
        magazines_data = cursor.fetchall()
        return magazines_data