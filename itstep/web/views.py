from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import authenticate, login as authLogin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Category, Post, Product, Purchase
from .forms import CustomUserCreationForm, ProductForm,User
from django.contrib.auth.forms import UserCreationForm
from .cart import Cart
# Create your views here.

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
    context = {'posts':posts}
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
    purchases = Purchase.objects.filter(user=user)
    context = {
        'user': user,
        'purchases': purchases,
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

@require_POST
def add_to_cart(request, item_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity)
    return redirect('cart')

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
    try:
        product = get_object_or_404(Product, id=item_id)
        cart.remove(product)
    except ValueError:
        pass
    return redirect('cart')

def about(request):
    context = {}
    return render(request,'web/about.html', context)

def services(request):
    context = {}
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