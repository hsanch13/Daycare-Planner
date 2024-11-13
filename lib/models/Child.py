from __init__ import CURSOR, CONN
from parent import Parent

class Child:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, gender, age, id=None):
        self.id = id
        self.name = name
        self.gender = gender
        self.age = age

    # def __repr__(self):
    #     return (
    #         f"<Employee {self.id}: {self.name}, {self.job_title}, " +
    #         f"Department ID: {self.department_id}>"
    #     )


########### PROPERTIES
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("your name must be a string")
        elif not len(name) in range(1, 26):
            raise ValueError("your name must be between 1 and 25 characters")
        else:
            self._name = name


    @property
    def gender(self):
        return self._gender.upper()

    @gender.setter
    def gender(self, gender):
        if not isinstance(gender, str):
            raise TypeError("your gender must be a string")
        elif not ["Male", "Female", "Other"]:
            raise ValueError("your gender must be 'Male', 'Female' or 'Other'")
        else:
            self._gender = gender

    @property
    def age(self):
        return self._phone
    
    @age.setter
    def age(self, age):
        if not isinstance(age, int):
            raise TypeError("your age must be a number")
        else:
            self._phone = age


########## CLASS METHODS - CRUD
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Child instances """
        sql = """
            CREATE TABLE IF NOT EXISTS children (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            age INTEGER,
            FOREIGN KEY (department_id) REFERENCES parents(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Child instances """
        sql = """
            DROP TABLE IF EXISTS children;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, gender, and age id values of the current Child object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO children (name, gender, age)
                VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.gender, self.age))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Child instance."""
        sql = """
            UPDATE children
            SET name = ?, gender = ?, age = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.gender, self.age, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Child instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM children
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, name, gender, age):
        """ Initialize a new Child instance and save the object to the database """
        child = cls(name, gender, age)
        child.save()
        return child

    @classmethod
    def instance_from_db(cls, row):
        """Return an Child object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        child = cls.all.get(row[0])
        if child:
            # ensure attributes match row values in case local instance was modified
            child.name = row[1]
            child.gender = row[2]
            child.age = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            child = cls(row[1], row[2], row[3])
            child.id = row[0]
            cls.all[child.id] = child
        return child

    @classmethod
    def get_all(cls):
        """Return a list containing one Child object per table row"""
        sql = """
            SELECT *
            FROM children
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]


########## filer methods

######## check methods below
    @classmethod
    def find_by_age(cls, age):
        """Return Child object corresponding to the table row matching the specified age"""
        sql = """
            SELECT *
            FROM employees
            WHERE age = ?
        """

        row = CURSOR.execute(sql, (age,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return Child object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM children
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None