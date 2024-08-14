from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('blog', views.blog, name='blog'),
    path('contact', views.contact, name='contact'),
    path('single', views.single, name='single'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('shop', views.shop, name='shop'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
]
