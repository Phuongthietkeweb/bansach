from django.shortcuts import render
from django.http import HttpResponse

def cart_view(request):
    """Xem giỏ hàng"""
    return HttpResponse('''
    <h1>🛒 Giỏ hàng của bạn</h1>
    <p>Giỏ hàng hiện tại đang trống.</p>
    <a href="/books/">Tiếp tục mua sắm</a> | 
    <a href="/">← Về trang chủ</a>
    ''')

def add_to_cart(request, book_id):
    """Thêm sách vào giỏ hàng"""
    return HttpResponse(f'''
    <h1>✅ Đã thêm sách ID {book_id} vào giỏ hàng</h1>
    <a href="/cart/">Xem giỏ hàng</a> | 
    <a href="/books/">Tiếp tục mua sắm</a>
    ''')

def remove_from_cart(request, book_id):
    """Xóa sách khỏi giỏ hàng"""
    return HttpResponse(f'''
    <h1>🗑️ Đã xóa sách ID {book_id} khỏi giỏ hàng</h1>
    <a href="/cart/">Xem giỏ hàng</a>
    ''')
