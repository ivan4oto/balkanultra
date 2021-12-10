"""balkanultra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('about', about_view, name='about'),
    path('results/<int:year>', results_view, name='results'),
    path('register/<str:race>', register_view, name='register'),
    path('success', success_view, name='success'),
    path('cancel', cancel_view, name='cancel'),
    path('checkout', checkout_view, name='checkout'),
    path('create_checkout_session/<str:race>', create_checkout_session_view, name='create_checkout_session'),
    path('config/', stripe_config),  # new
]
