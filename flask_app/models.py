from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

book_author = db.Table('book_author',
                       db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
                       db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
                       )

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.relationship('Category', backref=db.backref('books', lazy=True))
    authors = db.relationship('Author', secondary=book_author, lazy='subquery', backref=db.backref('books', lazy=True))

class BookInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False, unique=True)
    stock = db.Column(db.Integer, default=0)
    book = db.relationship('Book', backref=db.backref('inventory', uselist=False))