from django.http import JsonResponse
from .models import Book
from django.db.models import Count, Q

def book_list(request):
    books = Book.objects.select_related('category').prefetch_related('authors').all()
    data = [{"title": b.title, "category": b.category.name} for b in books]
    return JsonResponse({"books": data})

def stats_view(request):
    count = Book.objects.aggregate(total=Count('id'))
    return JsonResponse(count)