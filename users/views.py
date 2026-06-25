from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from blog.forms import PostForm
from blog.models import Post
from .forms import CustomUserCreationForm, CustomUserUpdateForm

# DmitriiProkofiev
# 6554495a

# user
# 6554495a

# admin
# 6554495a

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context=context)

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("post_list")
        else:
            error = "Неверный логин или пароль"
    return render(request, "users/login.html", context={"error": error})

def account_view(request):
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:account')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, "users/account.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('post_list')

def profile_view(request, pk):
    User = get_user_model()
    user = get_object_or_404(User,id=pk)
    posts = Post.objects.filter(author=user)
    context = {
        'profile': user,
        'posts': posts,
    }
    return render(request, 'users/profile.html', context)