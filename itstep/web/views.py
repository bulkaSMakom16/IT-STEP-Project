from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    return render(request, 'web/index.html', context)

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

def login(request):
    context = {}
    return render(request, 'web/login.html', context)