from django.urls import path

from store.views import *

urlpatterns = [
    path("", IndexView.as_view(), name='index')
]
