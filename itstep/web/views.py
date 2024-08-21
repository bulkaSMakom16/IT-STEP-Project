from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import authenticate, login as authLogin
from .models import Category, Post
from .forms import CustomUserCreationForm,User
from django.contrib.auth.forms import UserCreationForm

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