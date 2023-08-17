from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.views import View

from account.forms import LoginForm, RegisterForm


class LoginView(View):

    # render login page
    def get(self, request):
        form = LoginForm()
        return render(request, "account/form.html", {"form": form})

    # check user's data and log him in if corrects
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            if user is not None:
                login(request, user)
            return redirect("")

        return render(request, "account/form.html", {"form": form})


class LogoutView(View):

    # logout user
    def get(self, request):
        logout(request)
        return redirect("")


class RegisterView(View):

    # render register page
    def get(self, request):
        form = RegisterForm()
        return render(request, "account/form.html", {"form": form})

    # get the data from user's form and create user
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            return redirect("")

        return render(request, "account/form.html", {"form": form})
