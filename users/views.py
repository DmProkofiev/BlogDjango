from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserUpdateForm


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

# DmitriiProkofiev
# 6554495a

# user
# 6554495a
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
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
    return redirect('index')