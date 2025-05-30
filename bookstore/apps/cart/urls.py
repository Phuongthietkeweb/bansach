from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='detail'),                    # /cart/ - Xem giỏ hàng
    path('add/<int:book_id>/', views.add_to_cart, name='add'),   # /cart/add/1/ - Thêm vào giỏ
    path('remove/<int:book_id>/', views.remove_from_cart, name='remove'), # /cart/remove/1/ - Xóa khỏi giỏ
] 