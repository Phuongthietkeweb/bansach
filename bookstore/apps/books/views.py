from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Book, Category
from .forms import CustomUserCreationForm


def book_list_view(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_slug = request.GET.get('category')

    books = Book.objects.all()
    categories = Category.objects.filter(is_active=True)
    selected_category = None

    # Lưu total_books trước khi filter để hiển thị thông tin
    total_books = books.count()

    if query:
        books = books.filter(title__icontains=query)
    if min_price:
        books = books.filter(price__gte=min_price)
    if max_price:
        books = books.filter(price__lte=max_price)
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=selected_category)

    # Đếm số sách sau khi filter
    filtered_books_count = books.count()

    # Pagination với 12 sách mỗi trang (chia hết cho grid)
    paginator = Paginator(books.order_by('title'), 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tính toán range hiển thị
    start_index = (page_obj.number - 1) * paginator.per_page + 1
    end_index = min(start_index + paginator.per_page - 1, filtered_books_count)

    # Tạo URL parameters để giữ filter khi chuyển trang
    filter_params = {}
    if query:
        filter_params['q'] = query
    if min_price:
        filter_params['min_price'] = min_price
    if max_price:
        filter_params['max_price'] = max_price
    if category_slug:
        filter_params['category'] = category_slug

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'total_books': total_books,
        'filtered_books_count': filtered_books_count,
        'start_index': start_index,
        'end_index': end_index,
        'filter_params': filter_params,
        'has_filters': bool(query or min_price or max_price or category_slug),
        'page_title': f'Sách - {selected_category.name}' if selected_category else 'Danh Sách Sách',
    }
    return render(request, 'books/book_list.html', context)


def book_detail_view(request, slug):
    book = get_object_or_404(Book, slug=slug)
    
    # Lấy các sách cùng category (trừ sách hiện tại)
    related_books = []
    if book.category:
        related_books = Book.objects.filter(
            category=book.category
        ).exclude(slug=slug)[:6]  # Lấy tối đa 6 sách liên quan
    
    context = {
        'book': book,
        'related_books': related_books,
        'page_title': book.title,
    }
    return render(request, 'books/book_detail.html', context)


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tạo tài khoản thành công!")
            return redirect('books:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})


def logout_view(request):
    """Custom logout view to show success page"""
    logout(request)
    return render(request, 'user/logout.html')


@login_required
def profile_view(request):
    return render(request, 'user/profile.html')

