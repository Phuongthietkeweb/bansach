from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')  # Hiện thêm cột
    list_filter = ('is_staff', 'is_superuser', 'is_active')        # Bộ lọc bên phải
    search_fields = ('username', 'email')                         # Tìm kiếm theo username, email

admin.site.unregister(User)  # Unregister trước để tránh conflict
admin.site.register(User, CustomUserAdmin)
