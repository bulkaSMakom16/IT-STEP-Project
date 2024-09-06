from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import authenticate, login as authLogin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Category, Post, Product, Service
from .forms import CustomUserCreationForm, OrderForm, PostForm, ProductForm, ServiceForm, SubscriberForm,User
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileUpdateForm, CustomPasswordChangeForm
from .cart import Cart
from .models import PurchasedProduct
# Create your views here.


def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully subscribed!")
            return redirect('index')
        else:
            messages.error(request, "There was an error with your subscription.")
    else:
        form = SubscriberForm()
    return render(request, 'subscribe.html', {'form': form})

@staff_member_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ServiceForm()
    return render(request, 'web/add_service.html', {'form': form})

@staff_member_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'web/create_post.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'web/register.html', {'form': form})

def getCategories():
    all = Category.objects.all()
    count = all.count()
    half = count // 2
    firstHalf = all[:half]
    secondHalf = all[half:]
    return{'cats1':firstHalf, 'cats2':secondHalf}

def category(request, c=None):
    cObj = get_object_or_404(Category, name=c)
    posts = Post.objects.filter(category=cObj).order_by("-publishedDate")
    context = {'posts':posts}
    context.update(getCategories())
    return render(request, 'web/index.html', context)


def index(request):
    posts = Post.objects.all()
    services = Service.objects.all()
    context = {'posts':posts,
               'services': services}
    context.update(getCategories())
    return render(request, 'web/index.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'web/login.html')

@login_required
def profile_view(request):
    user = request.user
    purchased_products = PurchasedProduct.objects.filter(user=request.user)
    context = {
        'user': user,
        'purchased_products': purchased_products,
    }
    return render(request, 'web/profile.html', context)

def shop_view(request):
    products = Product.objects.all()
    if request.user.is_staff:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('shop')
        else:
            form = ProductForm()
        return render(request, 'web/shop.html', {'products': products, 'form': form})
    else:
        return render(request, 'web/shop.html', {'products': products})
    
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'web/product_detail.html', {'product': product})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop')
    else:
        form = ProductForm()
    
    context = {
        'form': form
    }
    return render(request, 'web/add_product.html', context)

@login_required
def checkout_page(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        products = Product.objects.filter(id__in=cart.keys())

        for product in products:
            PurchasedProduct.objects.create(
                user=request.user,
                product=product,
            )

        request.session['cart'] = {}
        request.session.modified = True
        return redirect('profile')

    else:
        cart = request.session.get('cart', {})
        products = Product.objects.filter(id__in=cart.keys())
        form = OrderForm()

    return render(request, 'web/checkout.html', {'form': form, 'products': products})


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        
        if 'update_profile' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'There was an error updating your profile.')

        if 'change_password' in request.POST:
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Your password has been updated successfully.')
                return redirect('update_profile')
            else:
                messages.error(request, 'There was an error changing your password.')
    else:
        profile_form = ProfileUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    context = {
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'web/update_profile.html', context)

@require_POST
def add_to_cart(request, item_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity)
    return redirect('cart')

def cart_view(request):
    cart = Cart(request)
    context = {
        'cart': cart,
        'cart_count': cart.get_total_items(),
    }
    return render(request, 'web/cart.html', context)

@require_POST
def update_cart(request, item_id):
    item_id = str(item_id)
    if not item_id.isdigit():
        return redirect('cart')
    
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    if quantity <= 0:
        cart.pop(item_id, None)
    else:
        if item_id in cart:
            cart[item_id]['quantity'] = quantity
    request.session['cart'] = cart
    return redirect('cart')

@require_POST
def remove_from_cart(request, item_id):
    item_id = str(item_id)
    if not item_id.isdigit():
        return redirect('cart')
    cart = Cart(request)
    cart.remove_item(item_id)
    return redirect('cart')

def about(request):
    context = {}
    return render(request,'web/about.html', context)

def services(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'web/services.html', context)

def blog(request):
    context = {}
    return render(request, 'web/blog.html', context)

def contact(request):
    context = {}
    return render(request, 'web/contact.html', context)

def single(request):
    context = {}
    return render(request, 'web/single.html', context)

def shop(request):
    context = {}
    return render(request, 'web/shop.html', context)

def cart(request):
    context = {}
    return render(request, 'web/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'web/checkout.html', context)