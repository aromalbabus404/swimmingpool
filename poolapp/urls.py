from django.urls import path
from . import views

urlpatterns = [

    # Website
    path('', views.index, name='index'),

    # Hidden Admin Login
    path('manager-2026/', views.admin_login, name='admin_login'),

    # Dashboard
    path('manager-2026/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Logout
    path('manager-2026/admin_logout/', views.admin_logout, name='admin_logout'),
]