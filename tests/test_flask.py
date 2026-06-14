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

def test_flask_route(client, app):
    with app.app_context():
        response = client.get('/books')
        assert response.status_code == 200

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