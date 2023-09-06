from django.contrib import admin
from store.models import *

admin.site.register([Customer, Category, Product, ProductImage, Order, OrderItem, ShippingAddress])

