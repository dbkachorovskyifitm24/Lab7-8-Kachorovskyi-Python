import pytest
from unittest.mock import patch
from django.db.utils import IntegrityError
from library.models import Category, Author, Book, BookInventory


@pytest.mark.django_db
def test_category_creation():
    cat = Category.objects.create(name="Science Fiction")
    assert str(cat) == "Science Fiction"
    assert cat.name == "Science Fiction"


@pytest.mark.django_db
def test_book_relations():
    cat = Category.objects.create(name="IT")
    author = Author.objects.create(name="Guido van Rossum")
    book = Book.objects.create(title="Python Basics", category=cat, price=10.0)
    book.authors.add(author)
    inv = BookInventory.objects.create(book=book, stock=5)

    assert book.category == cat
    assert author in book.authors.all()
    assert book.inventory.stock == 5


@pytest.mark.django_db
@pytest.mark.parametrize("name, expected", [
    ("Math", "Math"),
    ("Physics", "Physics"),
    ("Art", "Art"),
])
def test_category_parametrize(name, expected):
    cat = Category.objects.create(name=name)
    assert str(cat) == expected


@pytest.mark.django_db
def test_category_unique_constraint():
    Category.objects.create(name="Unique")
    with pytest.raises(IntegrityError):
        Category.objects.create(name="Unique")


@pytest.mark.django_db
def test_book_list_view(django_client):
    Category.objects.create(name="TestCat")
    response = django_client.get('/books/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_invalid_url_django(django_client):
    response = django_client.get('/invalid-url/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_book_create_view(django_client):
    import json
    payload = json.dumps({"title": "New Book", "category": "Tech", "price": "29.99", "stock": 10})
    response = django_client.post(
        '/books/create/',
        data=payload,
        content_type='application/json'
    )
    assert response.status_code == 201
    assert response.json()["title"] == "New Book"


@pytest.mark.django_db
def test_book_detail_not_found(django_client):
    response = django_client.get('/books/9999/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_search_view(django_client):
    cat = Category.objects.create(name="Fantasy")
    Book.objects.create(title="The Hobbit", category=cat, price=15.0)
    response = django_client.get('/books/search/?q=hobbit')
    assert response.status_code == 200
    assert len(response.json()["results"]) == 1


@patch('library.views.Book.objects.aggregate')
@pytest.mark.django_db
def test_mock_aggregate(mock_agg, django_client):
    mock_agg.return_value = {'total': 99, 'avg_price': None}
    response = django_client.get('/stats/')
    assert response.json()['totals']['total'] == 99
    mock_agg.assert_called_once()


@patch('requests.get')
def test_mock_external_api(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"isbn": "12345", "title": "Remote Book"}

    import requests
    result = requests.get("https://api.openlibrary.org/books/12345.json")

    assert result.status_code == 200
    assert result.json()["isbn"] == "12345"
    mock_get.assert_called_once_with("https://api.openlibrary.org/books/12345.json")