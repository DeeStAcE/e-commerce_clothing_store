from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from store.views import *

urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path("add-product/", AddProductView.as_view(), name='add_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
