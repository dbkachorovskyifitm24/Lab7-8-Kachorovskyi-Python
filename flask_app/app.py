from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Book, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{"title": b.title, "category": b.category.name} for b in books])


@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    try:
        cat = Category.query.filter_by(name=data['category']).first()
        if not cat:
            cat = Category(name=data['category'])
            db.session.add(cat)
        book = Book(title=data['title'], price=data['price'], category=cat)
        db.session.add(book)
        db.session.commit()
        return jsonify({"id": book.id, "title": book.title}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)