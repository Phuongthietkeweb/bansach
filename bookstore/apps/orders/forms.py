from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone',
            'address', 'city', 'district', 'ward',
            'payment_method', 'notes'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nhập họ và tên đầy đủ'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'example@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '0123456789'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Số nhà, tên đường...'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Tỉnh/Thành phố'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Quận/Huyện'
            }),
            'ward': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Phường/Xã'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Ghi chú đặc biệt (tuỳ chọn)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Nếu user đã đăng nhập, tự động điền thông tin
        if user and user.is_authenticated:
            self.fields['full_name'].initial = f"{user.first_name} {user.last_name}".strip()
            self.fields['email'].initial = user.email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Xóa khoảng trắng và ký tự đặc biệt
            phone = ''.join(filter(str.isdigit, phone))
            if len(phone) < 10 or len(phone) > 11:
                raise forms.ValidationError('Số điện thoại không hợp lệ.')
        return phone 