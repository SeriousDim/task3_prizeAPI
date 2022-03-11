"""promos URL Configuration

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

from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('promo', promo),
    path('promo/<int:id>', specific_promo),
    path('promo/<int:id>', edit_promo),
    path('promo/<int:id>', delete_promo),
    path('promo/<int:id>/participant', add_part),
    path('promo/<int:promo_id>/participant/<int:part_id>', delete_part),
    path('promo/<int:id>/prize', prize),
    path('promo/<int:promo_id>/prize/<int:prize_id>', prize),
    path('promo/<int:id>/raffle', start)
]
