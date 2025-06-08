from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên Danh Mục")
    description = models.TextField(blank=True, null=True, verbose_name="Mô Tả")
    slug = models.SlugField(unique=True, max_length=200, blank=True, null=True, verbose_name="Slug")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày Tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày Cập Nhật")
    is_active = models.BooleanField(default=True, verbose_name="Kích Hoạt")

    class Meta:
        verbose_name = "Danh Mục"
        verbose_name_plural = "Danh Mục"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_books_count(self):
        return self.book_set.count()
    get_books_count.short_description = 'Số Sách'

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tên Sách")
    author = models.CharField(max_length=100, verbose_name="Tác Giả")
    slug = models.SlugField(unique=True, max_length=200, blank=True, null=True) 
    description = models.TextField(verbose_name="Mô Tả")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá")
    discount = models.DecimalField(max_digits=5, decimal_places=0, default=0.00, verbose_name="Giảm Giá (%)")
    stock = models.IntegerField(verbose_name="Số Lượng Tồn Kho")
    image = models.ImageField(upload_to='books/', blank=True, null=True, verbose_name="Hình Ảnh")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Thể Loại", null=True, blank=True)

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

    def get_discounted_price(self):
        """Tính giá sau khi giảm giá"""
        if self.discount > 0:
            discount_amount = (self.price * self.discount) / 100
            return self.price - discount_amount
        return self.price
