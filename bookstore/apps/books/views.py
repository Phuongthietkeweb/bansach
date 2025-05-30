from django.shortcuts import render
from django.http import HttpResponse

def book_list_view(request):
    """Danh sách sách"""
    return HttpResponse('''
    <h1>📚 Danh sách sách</h1>
    <p>Hiện tại chưa có sách nào. Vui lòng quay lại sau!</p>
    <a href="/">← Về trang chủ</a>
    ''')

def book_detail_view(request, slug):
    """Chi tiết sách"""
    return HttpResponse(f'''
    <h1>📖 Chi tiết sách: {slug}</h1>
    <p>Thông tin chi tiết về cuốn sách này sẽ hiển thị ở đây.</p>
    <a href="/books/">← Về danh sách sách</a>
    ''')
