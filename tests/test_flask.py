import pytest
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
from models import db, Category, Book


def test_flask_models(app):
    with app.app_context():
        cat = Category(name="History")
        db.session.add(cat)
        db.session.commit()
        assert Category.query.count() == 1


def test_flask_unique_constraint(app):
    with app.app_context():
        cat1 = Category(name="Duplicate")
        db.session.add(cat1)
        db.session.commit()
        cat2 = Category(name="Duplicate")
        db.session.add(cat2)
        with pytest.raises(IntegrityError):
            db.session.commit()


def test_flask_create_book_transaction(app):
    """Транзакційний сценарій: rollback при помилці"""
    with app.app_context():
        cat = Category(name="Science")
        db.session.add(cat)
        db.session.commit()
        try:
            book = Book(title="Bad Book", price=None, category=cat)  # price=None порушує NOT NULL
            db.session.add(book)
            db.session.commit()
        except Exception:
            db.session.rollback()
        assert Book.query.count() == 0


def test_flask_route(client, app):
    with app.app_context():
        response = client.get('/books')
        assert response.status_code == 200


def test_flask_create_route(client, app):
    with app.app_context():
        response = client.post('/books', json={
            "title": "Flask Book",
            "category": "Tech",
            "price": 19.99
        })
        assert response.status_code == 201
        assert response.get_json()["title"] == "Flask Book"


def test_invalid_url_flask(client, app):
    with app.app_context():
        response = client.get('/non-existent')
        assert response.status_code == 404


@patch('models.Book.query')
def test_mock_flask_query(mock_query, client, app):
    mock_query.all.return_value = []
    response = client.get('/books')
    assert response.status_code == 200
    mock_query.all.assert_called_once()