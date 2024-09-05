from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('blog', views.blog, name='blog'),
    path('contact', views.contact, name='contact'),
    path('single', views.single, name='single'),
    path('register', views.register, name='register'),
    path('shop', views.shop_view, name='shop'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout_page, name='checkout_page'),
    path('login', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('add/', views.add_product, name='add_product'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('create-post/', views.create_post, name='create_post'),
    path('subscribe/', views.subscribe, name='subscribe'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
