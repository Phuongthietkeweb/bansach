from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('book', 'quantity', 'price', 'get_total_price')
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price():,.0f}₫"
    get_total_price.short_description = 'Thành tiền'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone', 'status', 'payment_method', 'total_amount', 'shipping_fee', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at', 'city']
    search_fields = ['id', 'full_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'get_total_with_shipping']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('user', 'status', 'payment_method')
        }),
        ('Thông tin khách hàng', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Địa chỉ giao hàng', {
            'fields': ('address', 'ward', 'district', 'city')
        }),
        ('Thông tin thanh toán', {
            'fields': ('total_amount', 'shipping_fee', 'get_total_with_shipping')
        }),
        ('Ghi chú', {
            'fields': ('notes',)
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_total_with_shipping(self, obj):
        return f"{obj.get_total_with_shipping():,.0f}₫"
    get_total_with_shipping.short_description = 'Tổng tiền (bao gồm ship)'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Khi tạo mới
            obj.save()
        else:  # Khi cập nhật
            obj.save()

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity', 'price', 'get_total_price']
    list_filter = ['order__created_at', 'book__category']
    search_fields = ['order__id', 'book__title', 'order__full_name']
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price():,.0f}₫"
    get_total_price.short_description = 'Thành tiền'
