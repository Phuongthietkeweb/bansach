from django.shortcuts import render
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

# Create your views here.
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
from django.contrib.auth.models import User
from django.shortcuts import render

def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})
