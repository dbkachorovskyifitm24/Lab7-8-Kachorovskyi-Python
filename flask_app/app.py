from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)