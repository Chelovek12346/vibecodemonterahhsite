from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("iuu:profile")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.get_full_name()}!")
            return redirect("iuu:profile")
    else:
        form = RegisterForm()

    return render(request, "iuu/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("iuu:profile")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Вы вошли как {user.get_full_name() or user.username}.")
            next_url = request.GET.get("next") or request.POST.get("next", "")
            if next_url and next_url.startswith("/"):
                return redirect(next_url)
            return redirect("iuu:profile")
    else:
        form = LoginForm(request)

    return render(request, "iuu/login.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "Вы вышли из аккаунта.")
        return redirect("iuu:login")
    return redirect("iuu:profile")


@login_required
def profile_view(request):
    return render(request, "iuu/profile.html", {"user": request.user})


def home_view(request):
    return render(request, "iuu/home.html", {"user": request.user})