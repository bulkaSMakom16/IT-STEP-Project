from django.contrib import admin
from .models import Post, Category,Product, Service

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Service)