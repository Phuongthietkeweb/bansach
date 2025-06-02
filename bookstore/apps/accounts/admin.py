from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

# Tùy chỉnh hiển thị cột trong bảng admin
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'is_staff', 'is_superuser',
        'is_active', 'date_joined', 'last_login'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')

# Gỡ đăng ký mặc định và đăng ký lại với CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
