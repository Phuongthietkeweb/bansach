
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'birthday')
    search_fields = ('user__username', 'full_name')

admin.site.register(UserProfile, UserProfileAdmin)
 

# apps/books/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock', 'slug', 'image_tag')
    list_editable = ('price', 'stock',)
    list_filter = ('author', 'stock',)
    search_fields = ('title', 'author', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('image_tag',) 

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'image', 'image_tag'),
        }),
        ('Thông tin chi tiết', {
            'fields': ('description', 'price', 'stock'),
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "Không có ảnh"
    image_tag.short_description = 'Ảnh Sách'
    image_tag.allow_tags = True


