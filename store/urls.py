from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from store.views import *

urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path("product/<slug:product_slug>/", ProductView.as_view(), name='product_view'),
    path("cart/", CartView.as_view(), name='cart'),
    path("checkout/", CheckoutView.as_view(), name='checkout'),
    path("update_item/", UpdateItemView.as_view(), name='update_item'),
    path("add-product/", AddProductView.as_view(), name='add_product'),
]
