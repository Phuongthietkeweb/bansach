from django.shortcuts import render
from django.http import HttpResponse

def order_list_view(request):
    """Lịch sử đơn hàng"""
    return HttpResponse('''
    <h1>📋 Lịch sử đơn hàng</h1>
    <p>Bạn chưa có đơn hàng nào.</p>
    <a href="/books/">Mua sắm ngay</a> | 
    <a href="/">← Về trang chủ</a>
    ''')

def order_create_view(request):
    """Tạo đơn hàng"""
    return HttpResponse('''
    <h1>📝 Tạo đơn hàng mới</h1>
    <p>Chức năng tạo đơn hàng đang được phát triển.</p>
    <a href="/cart/">← Về giỏ hàng</a>
    ''')

def checkout_view(request):
    """Thanh toán"""
    return HttpResponse('''
    <h1>💳 Thanh toán</h1>
    <p>Trang thanh toán đang được phát triển.</p>
    <a href="/cart/">← Về giỏ hàng</a>
    ''')

def order_detail_view(request, order_id):
    """Chi tiết đơn hàng"""
    return HttpResponse(f'''
    <h1>📄 Chi tiết đơn hàng #{order_id}</h1>
    <p>Thông tin chi tiết đơn hàng sẽ hiển thị ở đây.</p>
    <a href="/orders/">← Về lịch sử đơn hàng</a>
    ''')
