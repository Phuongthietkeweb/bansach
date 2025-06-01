from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

def book_list_view(request):
    """Danh sách sách"""
    return HttpResponse('''
    <h1>📚 Danh sách sách</h1>
    <p>Hiện tại chưa có sách nào. Vui lòng quay lại sau!</p>
    <a href="/">← Về trang chủ</a>
    ''')

def book_detail_view(request, slug):
    """Chi tiết sách"""
    return HttpResponse(f'''
    <h1>📖 Chi tiết sách: {slug}</h1>
    <p>Thông tin chi tiết về cuốn sách này sẽ hiển thị ở đây.</p>
    <a href="/books/">← Về danh sách sách</a>
    ''')
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tạo tài khoản thành công!")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'user/profile.html')

@user_passes_test(lambda u: u.is_staff)
def user_list(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
    else:
        users = User.objects.all()
    return render(request, 'user/user_list.html', {'users': users})


@user_passes_test(lambda u: u.is_staff)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user != user:  # Không cho xóa chính mình
        user.delete()
    return redirect('books:user_list')
