from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from decimal import Decimal

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đã giao hàng'),
        ('delivered', 'Đã nhận hàng'),
        ('cancelled', 'Đã hủy'),
    ]
    
    PAYMENT_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng'),
    ]
    
    # Thông tin khách hàng
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Khách hàng")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    
    # Địa chỉ giao hàng
    address = models.TextField(verbose_name="Địa chỉ")
    city = models.CharField(max_length=100, verbose_name="Tỉnh/Thành phố")
    district = models.CharField(max_length=100, verbose_name="Quận/Huyện")
    ward = models.CharField(max_length=100, verbose_name="Phường/Xã")
    
    # Thông tin đơn hàng
    total_amount = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Tổng tiền")
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Phí vận chuyển")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod', verbose_name="Phương thức thanh toán")
    
    # Ghi chú
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    
    # Thời gian
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.full_name}"
    
    def get_total_with_shipping(self):
        return self.total_amount + self.shipping_fee
    
    def get_status_display_color(self):
        status_colors = {
            'pending': 'warning',
            'processing': 'info',
            'shipped': 'primary',
            'delivered': 'success',
            'cancelled': 'danger',
        }
        return status_colors.get(self.status, 'secondary')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Đơn hàng")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Sách")
    quantity = models.PositiveIntegerField(verbose_name="Số lượng")
    price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Giá")
    
    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"
    
    def __str__(self):
        return f"{self.book.title} x {self.quantity}"
    
    def get_total_price(self):
        return self.price * self.quantity
