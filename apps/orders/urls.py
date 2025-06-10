from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list_view, name='list'),                # /orders/ - Lịch sử đơn hàng
    path('create/', views.order_create_view, name='create'),     # /orders/create/ - Tạo đơn hàng
    path('checkout/', views.checkout_view, name='checkout'),     # /orders/checkout/ - Thanh toán
    path('<int:order_id>/', views.order_detail_view, name='detail'), # /orders/1/ - Chi tiết đơn hàng
] 