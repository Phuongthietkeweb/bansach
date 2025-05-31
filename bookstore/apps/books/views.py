# apps/books/views.py

from django.shortcuts import render, get_object_or_404
from .models import Book

def book_list_view(request):
    """
    Hiển thị danh sách tất cả các cuốn sách trên trang chủ.
    """
    books = Book.objects.all().order_by('title')
    context = {
        'books': books,
        'page_title': 'Danh Sách Sách',
    }
    return render(request, 'books/book_list.html', context) # Django sẽ tìm trong apps/books/templates/books

def book_detail_view(request, slug):
    """
    Hiển thị thông tin chi tiết của một cuốn sách.
    """
    book = get_object_or_404(Book, slug=slug) 
    context = {
        'book': book,
        'page_title': book.title,
    }
    return render(request, 'books/book_detail.html', context) # Django sẽ tìm trong apps/books/templates/books