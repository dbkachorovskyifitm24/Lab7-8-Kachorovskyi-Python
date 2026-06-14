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
@pytest.mark.parametrize("name, expected", [("Math", "Math"), ("Physics", "Physics"), ("Art", "Art")])
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

@patch('library.views.Book.objects.aggregate')
@pytest.mark.django_db
def test_mock_aggregate(mock_agg, django_client):
    mock_agg.return_value = {'total': 99}
    response = django_client.get('/stats/')
    assert response.json() == {'total': 99}
    mock_agg.assert_called_once()