from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'books'

urlpatterns = [
   
    # Phía người dùng
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),


    path('', views.book_list_view, name='list'),              # /books/ - Danh sách sách
    path('<slug:slug>/', views.book_detail_view, name='detail'), # /books/ten-sach/ - Chi tiết sách

]