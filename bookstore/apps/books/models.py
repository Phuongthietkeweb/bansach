from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tên Sách")
    author = models.CharField(max_length=100, verbose_name="Tác Giả")
    slug = models.SlugField(unique=True, max_length=200, blank=True, null=True) 
    description = models.TextField(verbose_name="Mô Tả")
    price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Giá")
    stock = models.IntegerField(verbose_name="Số Lượng Tồn Kho")
    image = models.ImageField(upload_to='books/', blank=True, null=True, verbose_name="Hình Ảnh")

    class Meta:
        verbose_name = "Sách"
        verbose_name_plural = "Sách"
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, verbose_name='Họ và tên', blank=True)
    phone = models.CharField(max_length=15, verbose_name='Số điện thoại', blank=True)
    address = models.TextField(verbose_name='Địa chỉ', blank=True)
    birthday = models.DateField(verbose_name='Ngày sinh', blank=True, null=True)

    def __str__(self):
        return f"Thông tin: {self.user.username}"
