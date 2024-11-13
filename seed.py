from models.__init__ import CONN, CURSOR
from models.Parent import Parent
from models.Child import Child

def seed_database():
    # Drop tables if they exist and create them again
    Child.drop_table()
    Parent.drop_table()
    Parent.create_table()
    Child.create_table()

    # Add parents for testing
    Parent.create("Alice Johnson", "alice@example.com", "1234567890")
    Parent.create("Bob Smith", "bob@example.com", "0987654321")
    Parent.create("Carol Williams", "carol@example.com", "2345678901")
    Parent.create("David Brown", "david@example.com", "3456789012")

    # Add children for testing
    Child.create("Charlie Johnson", "Male", 10, 1)  # child of Alice Johnson
    Child.create("Sophia Smith", "Female", 8, 2)    # child of Bob Smith
    Child.create("Michael Williams", "Male", 12, 3) # child of Carol Williams
    Child.create("Emma Brown", "Female", 6, 4)      # child of David Brown

# Run the seed function
seed_database()