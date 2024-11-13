from __init__ import CURSOR, CONN

class Parent:

    all = {}

    def __init__(self, name, email, phone, id=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone

    # def __repr__(self):
    #     return f"<Parent {self.id}: {self.name}, {self.email} {self.phone}>"

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
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        if not isinstance(email, str):
            raise TypeError("your email must be a string")
        elif not len(email) in range(5, 30):
            raise ValueError("your email must be between 1 and 140 characters")
        elif not hasattr(self, "_email"):
            raise ValueError("your email already exists")
        else:
            self._email = email


    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, phone):
        if not isinstance(phone, str):
            raise TypeError("your phone number must be a string")
        else:
            self._phone = phone



######### ORM CLASS METHODS 
    #CRUD

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Parent instances """
        sql = """
            CREATE TABLE IF NOT EXISTS parents (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone INTEGER)
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Parent instances """
        sql = """
            DROP TABLE IF EXISTS parents;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and location values of the current Parent instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO parents (name, email, phone)
            VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.email, self.phone))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self


    @classmethod
    def create(cls, name, email, phone):
        """ Initialize a new Parent instance and save the object to the database """
        parent = cls(name, email, phone)
        parent.save()
        return [parent]

    def update(self):
        """Update the table row corresponding to the current Parent instance."""
        sql = """
            UPDATE parents
            SET name = ?, email = ?, phone = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.email, self.phone))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Parent instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM parents
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
        """Return a Parent object having the attribute values from the table row."""

        # Check the dictionary for an existing instance using the row's primary key
        parent = cls.all.get(row[0])
        if parent:
            # ensure attributes match row values in case local instance was modified
            parent.name = row[1]
            parent.email = row[2]
            parent.phone = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            parent = cls(row[1], row[2], row[3])
            parent.id = row[0]
            cls.all[parent.id] = parent
        return parent


    @classmethod
    def get_all(cls):
        """Return a list containing a Parent object per row in the table"""
        sql = """
            SELECT *
            FROM parents
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]


    ######filters

############# double check method below    
    @classmethod
    def find_by_email(cls, email):
        """Return a Parent object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM parents
            WHERE email = ?
        """

        row = CURSOR.execute(sql, (email,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return a Parent object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM parents
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def child(self):
        """Return list of children associated with current parent"""
        sql = """
            SELECT * FROM children
            WHERE parent_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Child.instance_from_db(row) for row in rows
        ]