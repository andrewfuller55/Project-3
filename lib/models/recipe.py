# lib/models/recipe.py
from models.__init__ import CURSOR, CONN
from models.meal import Meal


class Recipe:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, category, meal_id, id=None):
        self.id = id
        self.name = name
        self.category = category
        self.meal_id = meal_id

    def __repr__(self):
        return (
            f"<Recipe {self.id}: {self.name}, {self.category}, " +
            f"Meal ID: {self.meal_id}>"
        )

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if isinstance(category, str) and len(category):
            self._category = category
        else:
            raise ValueError(
                "category must be a non-empty string"
            )

    @property
    def meal_id(self):
        return self._meal_id

    @meal_id.setter
    def meal_id(self, meal_id):
        # if type(meal_id) is int and Meal.find_by_id(meal_id):
        self._meal_id = meal_id
        # else:
        #     raise ValueError(
        #         "meal_id must reference a meal in the database")

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Recipe instances """
        sql = """
            CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            meal_id INTEGER,
            FOREIGN KEY (meal_id) REFERENCES meals(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Recipe instances """
        sql = """
            DROP TABLE IF EXISTS recipes;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, job title, and department id values of the current Recipe object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO recipes (name, category, meal_id)
                VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.category, self.meal_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Recipe instance."""
        sql = """
            UPDATE recipes
            SET name = ?, category = ?, meal_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.category,
                             self.meal_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Recipe instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM recipes
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, name, category, meal_id):
        """ Initialize a new Recipe instance and save the object to the database """
        recipe = cls(name, category, meal_id)
        recipe.save()
        return recipe

    @classmethod
    def instance_from_db(cls, row):
        """Return an Recipe object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        recipe = cls.all.get(row[0])
        if recipe:
            # ensure attributes match row values in case local instance was modified
            recipe.name = row[1]
            recipe.category = row[2]
            recipe.meal_id = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            recipe = cls(row[1], row[2], row[3])
            recipe.id = row[0]
            cls.all[recipe.id] = recipe
        return recipe

    @classmethod
    def get_all(cls):
        """Return a list containing one Recipe object per table row"""
        sql = """
            SELECT *
            FROM recipes
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Recipe object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM recipes
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return Recipe object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM recipes
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None