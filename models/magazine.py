class Magazine:
    def __init__(self, id, name, category=None):
        """
        Initializes a Magazine instance.

        Args:
            id (int): The ID of the magazine.
            name (str): The name of the magazine.
            category (str): The category of the magazine.
        """
        self._id = id
        self._name = name
        self._category = category



    @property
    def id(self):
        """
        Gets the ID of the magazine.

        Returns:
            int: The ID of the magazine.
        """
        return self._id



    @property
    def name(self):
        """
        Get the name of the magazine.

        Returns:
            str: The name of the magazine.
        """
        return self._name



    @name.setter
    def name(self, value):
        """
        Sets the name of the magazine.

        Args:
            value (str): The name of the magazine.

        Raises:
            ValueError: If the name is not a string or not between 2 and 16 characters.
        """
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters")



    @property
    def category(self):
        """
        Gets the category of the magazine.

        Returns:
            str: The category of the magazine.
        """
        return self._category



    @category.setter
    def category(self, value):
        """
        Sets the category of the magazine.

        Args:
            value (str): The category of the magazine.

        Raises:
            ValueError: If the category is not a string or is an empty string.
        """
        if not isinstance(value, str):
            raise ValueError("Category must be a string")
        self._category = value
    
    
        
    def create(self, cursor):
        """
        Creates a new magazine in the database.

        Args:
            cursor: The database cursor.

        Returns:
            cursor: The database cursor.
        """
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self._name, self._category))
        self._id = cursor.lastrowid
        return cursor



    @classmethod
    def get_all(cls, cursor):
        """
        Gets all magazines from the database.

        Args:
            cursor: The database cursor.

        Returns:
            list: A list of Magazine instances.
        """
        cursor.execute("SELECT * FROM magazines")
        all_magazines = cursor.fetchall()
        return [cls(magazine_data[0], magazine_data[1], magazine_data[2]) for magazine_data in all_magazines]



    def get_articles(self, cursor):
        """
        Gets all articles associated with the magazine from the database.

        Args:
            cursor: The database cursor.

        Returns:
            list: A list of article data tuples.
        """
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self._id,))
        articles_data = cursor.fetchall()
        return articles_data



    def get_contributors(self, cursor):
        """
        Gets all authors who have contributed to the magazine from the database.

        Args:
            cursor: The database cursor.

        Returns:
            list: A list of author data tuples.
        """
        cursor.execute("""
            SELECT authors.*
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self._id,))
        contributors_data = cursor.fetchall()
        return contributors_data



    def get_article_titles(self, cursor):
        """
        Gets a list of article titles associated with the magazine from the database.

        Args:
            cursor: The database cursor.

        Returns:
            list: A list of article titles, or None if no titles are found.
        """
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self._id,))
        titles = [row[0] for row in cursor.fetchall()]
        return titles if titles else None



    def get_contributing_authors(self, cursor):
        """
        Gets a list of authors who have contributed more than two articles to the magazine from the database.

        Args:
            cursor: The database cursor.

        Returns:
            list: A list of author data tuples, or None if no contributing authors are found.
        """
        cursor.execute("""
            SELECT authors.*, COUNT(*) AS article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self._id,))
        authors_data = cursor.fetchall()
        return authors_data if authors_data else None