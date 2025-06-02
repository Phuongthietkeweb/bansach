from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

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

    """Chi tiết sách"""
    return HttpResponse(f'''
    <h1>📖 Chi tiết sách: {slug}</h1>
    <p>Thông tin chi tiết về cuốn sách này sẽ hiển thị ở đây.</p>
    <a href="/books/">← Về danh sách sách</a>
    ''')
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tạo tài khoản thành công!")
            return redirect('books:login')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'user/profile.html')

@user_passes_test(lambda u: u.is_staff)
def user_list(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
    else:
        users = User.objects.all()
    return render(request, 'user/user_list.html', {'users': users})


@user_passes_test(lambda u: u.is_staff)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user != user:  # Không cho xóa chính mình
        user.delete()
    return redirect('books:user_list')

    """
    Hiển thị thông tin chi tiết của một cuốn sách.
    """
    book = get_object_or_404(Book, slug=slug) 
    context = {
        'book': book,
        'page_title': book.title,
    }
    return render(request, 'books/book_detail.html', context) # Django sẽ tìm trong apps/books/templates/books

