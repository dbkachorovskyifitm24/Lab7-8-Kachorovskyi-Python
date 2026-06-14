import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Q, Avg

from .models import Book, Category, Author, BookInventory


def book_list(request):
    books = Book.objects.select_related('category').prefetch_related('authors').all()
    data = [{"title": b.title, "category": b.category.name} for b in books]
    return JsonResponse({"books": data})


def stats_view(request):
    totals = Book.objects.aggregate(total=Count('id'), avg_price=Avg('price'))
    by_category = list(
        Category.objects.annotate(book_count=Count('books')).values('name', 'book_count')
    )
    return JsonResponse({"totals": totals, "by_category": by_category})


def search_view(request):
    q = request.GET.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=q) | Q(category__name__icontains=q)
    ).select_related('category')
    data = [{"title": b.title, "category": b.category.name} for b in books]
    return JsonResponse({"results": data})


@csrf_exempt
@require_http_methods(["POST"])
def book_create(request):
    data = json.loads(request.body)
    cat, _ = Category.objects.get_or_create(name=data['category'])
    book = Book.objects.create(title=data['title'], category=cat, price=data['price'])
    BookInventory.objects.create(book=book, stock=data.get('stock', 0))
    return JsonResponse({"id": book.id, "title": book.title}, status=201)


@csrf_exempt
def book_detail(request, pk):
    try:
        book = Book.objects.select_related('category').get(pk=pk)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == 'GET':
        return JsonResponse({"id": book.id, "title": book.title, "price": str(book.price)})

    if request.method == 'PUT':
        data = json.loads(request.body)
        book.title = data.get('title', book.title)
        book.price = data.get('price', book.price)
        book.save()
        return JsonResponse({"id": book.id, "title": book.title})

    if request.method == 'DELETE':
        book.delete()
        return JsonResponse({"deleted": pk})