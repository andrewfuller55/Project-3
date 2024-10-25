# lib/models/meal.py
from models.__init__ import CURSOR, CONN


class Meal:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Meal {self.id}: {self.name}>"

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


    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Meal instances """
        sql = """
            CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY,
            name TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Meal instances """
        sql = """
            DROP TABLE IF EXISTS meals;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name value of the current Meal instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO meals (name)
            VALUES (?)
        """

        CURSOR.execute(sql, (self.name,))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name):
        """ Initialize a new Meal instance and save the object to the database """
        meal = cls(name)
        meal.save()
        return meal

    def update(self):
        """Update the table row corresponding to the current Meal instance."""
        sql = """
            UPDATE meals
            SET name = ?,
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Meal instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM meals
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """Return a Meal object having the attribute values from the table row."""

        # Check the dictionary for an existing instance using the row's primary key
        meal = cls.all.get(row[0])
        if meal:
            # ensure attributes match row values in case local instance was modified
            meal.name = row[1]

        else:
            # not in dictionary, create new instance and add to dictionary
            meal = cls(row[1])
            meal.id = row[0]
            cls.all[meal.id] = meal
        return meal

    @classmethod
    def get_all(cls):
        """Return a list containing a Meal object per row in the table"""
        sql = """
            SELECT *
            FROM meals
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return a Meal object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM meals
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return a Meal object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM meals
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def recipes(self):
        """Return list of recipes associated with current meal"""
        from models.recipe import Recipe
        sql = """
            SELECT * FROM recipes
            WHERE meal_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Recipe.instance_from_db(row) for row in rows
        ]