from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        ordering = ['name']
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=150, verbose_name="ПІБ")
    email = models.EmailField(blank=True, verbose_name="Email")
    bio = models.TextField(blank=True, verbose_name="Біографія")

    class Meta:
        ordering = ['name']
        verbose_name = "Автор"
        verbose_name_plural = "Автори"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    authors = models.ManyToManyField(Author, related_name='books')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ['-id']
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title


class BookInventory(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='inventory')
    stock = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Інвентар"
        verbose_name_plural = "Інвентар"

    def __str__(self):
        return f"{self.book.title} - {self.stock}"