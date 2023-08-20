from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.views import View
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q

from account.forms import LoginForm, RegisterForm
from account.tokens import account_activation_token


# email verification message
def activate_email(request, user, to_email):
    mail_subject = "Activate your user account"
    message = render_to_string("emails/email_verification.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])

    if email.send():
        messages.success(request,
                         f"Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and clickz \
                         received activation link to confirm and complete the registraton. \
                         <b>Note:</b> Check your spam folder")
    else:
        messages.error(request, f"Problem sending email to {to_email}, check if you typed it correctly.")


def get_user_from_email_verification_token(uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        return None

    if user is not None and account_activation_token.check_token(user, token):
        return user
    return None


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
            user.is_active = False
            user.set_password(form.cleaned_data["password1"])
            user.save()
            activate_email(request, user, form.cleaned_data.get("email"))
            return redirect("")

        return render(request, "account/form.html", {"form": form})


class ActivateUserView(View):

    def get(self, request, uidb64, token):
        user = get_user_from_email_verification_token(uidb64, token)
        if user:
            user.is_active = True
            user.save()

            messages.success(request, "Thank you for your email confirmation. Now you can login your account")
            return redirect("login")
        else:
            messages.error(request, "Activation link is invalid")

        return redirect("index")
