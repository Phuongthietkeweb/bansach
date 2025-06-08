from django.contrib import admin
from django.utils.html import format_html
from .models import Book, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_books_count', 'is_active', 'created_at', 'updated_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('get_books_count', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'is_active'),
        }),
        ('Thông tin chi tiết', {
            'fields': ('description',),
        }),
        ('Thống kê', {
            'fields': ('get_books_count', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def get_books_count(self, obj):
        count = obj.book_set.count()
        if count > 0:
            return format_html('<span style="color: green; font-weight: bold;">{} sách</span>', count)
        return format_html('<span style="color: red;">0 sách</span>')
    get_books_count.short_description = 'Số Sách'
    get_books_count.admin_order_field = 'book__count'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'discount', 'stock', 'slug', 'image_tag')
    list_editable = ('price', 'discount', 'stock', 'category')
    list_filter = ('category', 'author', 'stock')
    search_fields = ('title', 'author', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('image_tag', 'discounted_price_display') 

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category'),
        }),
        ('Nội dung', {
            'fields': ('description', 'image', 'image_tag'),
        }),
        ('Thông tin bán hàng', {
            'fields': ('price', 'discount', 'discounted_price_display', 'stock'),
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "Không có ảnh"
    image_tag.short_description = 'Ảnh Sách'
    image_tag.allow_tags = True

    def discounted_price_display(self, obj):
        """Hiển thị giá sau khi giảm giá"""
        try:
            discounted_price = obj.get_discounted_price()
            if obj.discount > 0:
                return format_html(
                    '<span style="color: red; font-weight: bold;">{} VNĐ</span> '
                    '<small style="color: gray;">(Giảm {}%)</small>',
                    int(discounted_price), obj.discount
                )
            return format_html('{} VNĐ', int(discounted_price))
        except Exception:
            return "Lỗi tính giá"
    discounted_price_display.short_description = 'Giá Sau Giảm'
    discounted_price_display.admin_order_field = 'price'


