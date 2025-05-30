from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list_view, name='list'),              # /books/ - Danh sách sách
    path('<slug:slug>/', views.book_detail_view, name='detail'), # /books/ten-sach/ - Chi tiết sách
] 