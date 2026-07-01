from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    return render(request, "index.html")


def admin_login(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect("admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect("admin_dashboard")
            else:
                messages.error(request, "You do not have permission to access the admin panel.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "admin_login.html")


@login_required(login_url="admin_login")
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


@login_required(login_url="admin_login")
def admin_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("admin_login")