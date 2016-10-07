"""MarketPlace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Crud import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^items/add/(?P<username>[A-Za-z0-9_]+)/', views.item_add, name='item_add'),
    url(r'^items/edit/(?P<username>[A-Za-z0-9_]+)/(?P<product_name>[A-Za-z0-9]+)/', 
        views.item_edit, name='item_edit'),
    url(r'^items/delete/(?P<username>[A-Za-z0-9_]+)/(?P<title>[A-Za-z0-9\[]+)/',
        views.item_delete, name='item_delete'),
    url(r'^items/detail/(?P<username>[A-Za-z0-9_]+)/',views.item_detail, name = 'item_detail'),
    url(r'^users/create/', views.user_create, name='user_create'),
    url(r'^users/update/(?P<username>[A-Za-z0-9_]+)/', views.user_update, name='user_update'),
    url(r'^users/read/(?P<username>[A-Za-z0-9_]+)/', views.user_read, name='user_read'),
    url(r'^users/delete/(?P<username>[A-Za-z0-9_]+)/', views.user_delete, name='user_delete'),
    url(r'^users/get/(?P<p_key>[0-9]+)/', views.user_get, name='user_get'),
    url(r'^login/(?P<username>[A-Za-z0-9_]+)/(?P<password>[A-Za-z0-9_]+)/',views.user_login, name='user_login'),
]
