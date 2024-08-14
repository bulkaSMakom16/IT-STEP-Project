from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('blog', views.blog, name='blog'),
    path('contact', views.contact, name='contact'),
    path('single', views.single, name='single'),
    path('login', views.login, name='login')
]
