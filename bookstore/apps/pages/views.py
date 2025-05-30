from django.shortcuts import render
from django.http import HttpResponse

def home_view(request):
    """Trang chủ"""
    return render(request, 'user/home.html', {
        'title': 'Trang chủ',
        'message': 'Chào mừng đến với Bookstore!'
    })

def about_view(request):
    """Trang giới thiệu"""
    return HttpResponse('<h1>Trang giới thiệu</h1><p>Đây là trang giới thiệu về Bookstore.</p>')

def contact_view(request):
    """Trang liên hệ"""
    return HttpResponse('<h1>Liên hệ</h1><p>Email: contact@bookstore.com</p>') 