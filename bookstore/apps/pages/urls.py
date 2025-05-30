from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home_view, name='home'),           # Trang chủ
    path('about/', views.about_view, name='about'),   # Giới thiệu
    path('contact/', views.contact_view, name='contact'), # Liên hệ
] 