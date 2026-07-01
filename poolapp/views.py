from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")


def admin_login(request):

    if request.user.is_authenticated:
        return redirect("admin_dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("admin_dashboard")

        else:

            messages.error(request, "Invalid Username or Password")

    return render(request, "admin_login.html")


@login_required(login_url="admin_login")
def admin_dashboard(request):

    return render(request, "admin_dashboard.html")


def logout_view(request):

    logout(request)

    return redirect("admin_login")