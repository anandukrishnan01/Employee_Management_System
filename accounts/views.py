from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, RegisterForm, PasswordChangeForm, UserProfileUpdateForm
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("employees:employee_list")

    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            login(request, form.user)
            return redirect("employees:employee_list")

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                email=data["email"],
                username=data["username"],
                password=data["password"],
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
                phone_number=data.get("phone_number", ""),
            )
            login(request, user)
            return redirect("employees:employee_list")

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def change_password(request):
    form = PasswordChangeForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            if not request.user.check_password(form.cleaned_data["old_password"]):
                messages.error(request, "Old password is incorrect.")
            else:
                request.user.set_password(form.cleaned_data["new_password"])
                request.user.save()
                messages.success(request, "Password changed successfully.")
                return redirect("accounts:login")

    return render(request, "accounts/change_password.html", {"form": form})


@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, "accounts/profile.html", {"profile": profile})


@login_required
def profile_update_view(request):
    profile = request.user.profile
    form = UserProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user
            obj.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")

    return render(request, "accounts/profile_update.html", {"form": form})
