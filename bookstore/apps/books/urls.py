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

    # Phía admin
    path('users/', views.user_list, name='user_list'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    path('', views.book_list_view, name='list'),              # /books/ - Danh sách sách
    path('<slug:slug>/', views.book_detail_view, name='detail'), # /books/ten-sach/ - Chi tiết sách

]