from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.contrib import messages

from store.forms import *
from store.models import *


class IndexView(View):

    def get(self, request):
        return render(request, "store/index.html")

    def post(self, request):
        pass


class AddProductView(PermissionRequiredMixin, View):
    permission_required = "product.add_product"

    def get(self, request):
        form = ProductForm()
        image_form = ProductImageForm()
        return render(request, "store/product_form.html", {"form": form, "image_form": image_form})

    def post(self, request):
        form = ProductForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            form.save()
            for file in files:
                ProductImage.objects.create(product=form, image=file)
            messages.success(request, "New product added successfully")
        else:
            messages.error(request, "Error during adding a new product. Try again")
            return render(request, "store/product_form.html", {"form": form})
        return redirect("index")
