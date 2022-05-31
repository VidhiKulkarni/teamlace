""" database dependencies to support Users db examples """
import os
import shutil
from random import randrange

from __init__ import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Define the 'Users Notes' table  with a relationship to Users within the model
class Notes(db.Model):
    __tablename__ = 'notes'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, userID, note, image):
        self.userID = userID
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "note": self.note,
            "userID": self.userID,
            "image": self.image
        }

    def update(self, note):
        """only updates values with length"""
        if len(note) > 0:
            self.note = note
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


# Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along

# Define the Users table within the model
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Users represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Users(UserMixin, db.Model):
    # define the Users schema
    userID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    role = db.Column(db.String(255), unique=False, nullable=False)
    grade = db.Column(db.Integer, unique=False, nullable=False)
    email = db.Column(db.String(255), unique=False, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    notes = db.relationship("Notes", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes of instance variables within object
    def __init__(self, name, role, grade, email, password):
        self.name = name
        self.role = role
        self.grade = grade
        self.email = email
        self.set_password(password)

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Users(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "userID": self.userID,
            "name": self.name,
            "role": self.role,
            "grade": self.grade,
            "email": self.email,
            "password": self.password,
            "notes": self.notes,
            "query": "by_alc"  # This is for fun, a little watermark
        }

    def read2(self):
        return {
            "userID": self.userID,
            "name": self.name,
            "role": self.role,
            "grade": self.grade,
            "email": self.email,
            "password": self.password,
            "query": "by_alc"  # This is for fun, a little watermark
        }

    # CRUD update: updates users name, password, phone
    # returns self
    def update(self, name, role="", grade="", email="", password=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(role) > 0:
            self.role = role
        if len(grade) > 0:
            self.grade = grade
        if len(email) > 0:
            self.email = email
        if len(password) > 0:
            self.set_password(password)
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    # set password method is used to create encrypted password
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    # check password to check versus encrypted password
    def is_password_match(self, password):
        """Check hashed password."""
        result = check_password_hash(self.password, password)
        return result

    # required for login_user, overrides id (login_user default) to implemented userID
    def get_id(self):
        return self.userID


"""Database Creation and Testing section"""


def model_builder():
    print("--------------------------")
    print("Seed Data for Table: users")
    print("--------------------------")
    db.create_all()
    """Tester data for table"""
    u1 = Users(name='Grace Wang', role="President", grade="10", email="abc@xyz.org", password='grace')
    u2 = Users(name='Vidhi Kulkarni', role="President", grade="10", email='vk@example.com', password='vidhi')
    u3 = Users(name='John Mortensen', role="Member", grade="1000", email='jmort1021@gmail.com', password='123qwerty')
    # U7 intended to fail as duplicate key
    u4 = Users(name='John Mortensen', role="Member", grade="1000", email='jmort1021@gmail.com', password='123qwerty')
    table = [u1, u2, u3, u4]
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {row.email}")

    # """Builds sample user/note(s) data"""
    # for row in table:
    #     # prime uploads foler
    #     try:
    #         os.makedirs('../volumes/uploads')
    #     except:
    #         pass
    #     shutil.copy("../static/assets/GIDASlogo.png", "../volumes/uploads")
    #     # add some notes with default image
    #     try:
    #         '''add a few 1 to 4 notes per user'''
    #         for num in range(randrange(1, 4)):
    #             note = "#### " + row.name + " note " + str(num) + ". \n Generated by test data."
    #             row.notes.append(Notes(userID=row.userID, note=note, image='GIDASlogo.png'))
    #         '''add user/note data to table'''
    #         db.session.add(row)
    #         db.session.commit()
    #     except IntegrityError:
    #         '''fails with bad or duplicate data'''
    #         db.session.remove()
    #         print(f"Records exist, duplicate email, or error: {row.email}")


def model_printer():
    print("------------")
    print("Table: users with SQL query")
    print("------------")
    result = db.session.execute('select * from users')
    print(result.keys())
    for row in result:
        print(row)

        # Looks into database


def model_driver():
    print("---------------------------")
    print("Create Tables and Seed Data")
    print("---------------------------")
    model_builder()

    print("---------------------------")
    print("Table: " + Users.__tablename__)
    print("Columns: ", Users.__table__.columns.keys())
    print("---------------------------")
    print("Table: " + Notes.__tablename__)
    print("Columns: ", Notes.__table__.columns.keys())
    print("---------------------------")
    print()

    users = Users.query
    for user in users:
        print("User" + "-" * 81)
        print(user.read())
        print("Notes" + "-" * 80)
        for note in user.notes:
            print(note.read())
        print("-" * 85)
        print()


if __name__ == "__main__":
    model_builder()
    model_printer()
    model_driver()
