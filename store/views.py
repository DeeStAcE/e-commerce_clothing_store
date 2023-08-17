from django.shortcuts import render, redirect
from django.views import View


class IndexView(View):

    def get(self, request):
        return render(request, "store/index.html")

    def post(self, request):
        pass
