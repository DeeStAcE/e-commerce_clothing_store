from django.contrib import admin
from store.models import *

admin.site.register([Product, Cart, CartProduct, Category, Order, ProductImage])
