from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
a="dafa"
a.capitalize()
class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(25),unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)

class Book(db.Model):
    __tablename__="books"
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String, nullable=False)
    author=db.Column(db.String, nullable=False)
    public_year=db.Column(db.Integer, nullable=False)
    isbn=db.Column(db.Integer, nullable=False)

class Review(db.Model):
    __tablename__="reviews"
    id=db.Column(db.Integer, primary_key=True)
    review=db.Column(db.String, nullable=False)
    book_id=db.Column(db.String, nullable=False)
    acc_id=db.Column(db.Integer, nullable=False)