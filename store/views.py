import json

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import JsonResponse

from store.forms import *
from store.models import *


class IndexView(View):

    def get(self, request):
        products = Product.objects.all()
        context = {
            'products': products
        }
        return render(request, "store/index.html", context)

    def post(self, request):
        pass


class ProductView(View):

    def get(self, request, product_slug):
        product = Product.objects.get(slug=product_slug)
        context = {
            'product': product
        }
        return render(request, "store/product_view.html", context)

    def post(self, request):
        pass


class CartView(View):

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {
                'get_cart_total': 0,
                'get_cart_items': 0
            }
        context = {
            'items': items,
            'order': order
        }
        return render(request, "store/cart.html", context)

    def post(self, request):
        pass


class CheckoutView(View):

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {
                'get_cart_total': 0,
                'get_cart_items': 0
            }
        context = {
            'items': items,
            'order': order
        }
        return render(request, "store/checkout.html", context)

    def post(self, request):
        pass


class UpdateItemView(View):

    def post(self, request):
        data = json.loads(request.body)
        product_id = data['productId']
        action = data['action']
        print(product_id, action)

        customer = request.user.customer
        product = Product.objects.get(pk=product_id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

        # managing the quantity of each item in a cart after clicking 'Add to Cart' button
        if action == 'add':
            order_item.quantity = (order_item.quantity + 1)
        elif action == 'remove':
            order_item.quantity = (order_item.quantity - 1)

        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()

        return JsonResponse('Item was added', safe=False)


# Form for adding a new product with multiple images at once (doesn't work for now)
class AddProductView(PermissionRequiredMixin, View):
    permission_required = "product.add_product"

    def get(self, request):
        form = ProductForm()
        image_form = FileFieldForm()
        return render(request, "store/product_form.html", {"form": form, "image_form": image_form})

    def post(self, request):
        form = ProductForm(request.POST)
        image_form = FileFieldForm(request.POST)

        if form.is_valid() and image_form.is_valid():
            new_product = form.save()
            files = image_form.cleaned_data["file_field"]
            print(files)

            for file in files:
                ProductImage.objects.create(product=new_product, image=file)
            messages.success(request, "New product added successfully")
        else:
            messages.error(request, "Error during adding a new product. Try again")
            return render(request, "store/product_form.html", {"form": form, "image_form": image_form})
        return redirect("index")
