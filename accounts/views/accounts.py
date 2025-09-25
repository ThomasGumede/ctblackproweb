from accounts.forms import UserLoginForm, RegistrationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from accounts.utilities.custom_emails import send_email_confirmation_email, send_html_email, send_verification_email
from django.shortcuts import redirect, render, get_object_or_404
from accounts.utilities.decorators import user_not_authenticated
from accounts.utilities.tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import logging, jwt



logger = logging.getLogger("accounts")
User = get_user_model()


@user_not_authenticated
def custom_login(request):
    next_page = request.GET.get("next", None)
    template_name = "accounts/login.html"
    success_url = "home:index"
    if next_page:
        success_url = next_page

    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None and user.is_active:
                login(request, user)
                messages.success(
                    request, f"Hello <b>{user.username}</b>! You have been logged in"
                )
                return redirect(success_url)
        else:
            account = User.objects.filter(username=form.cleaned_data["username"]).first()
            if account != None and not account.is_active:
                messages.error(request, f"Sorry your account is not active. We have sent account activation email to your email {account.email}")
                sent = send_verification_email(account, request)
                if not sent:
                    pass
                return redirect("accounts:login")
            
            return render(
                request=request, template_name=template_name, context={"form": form}
            )

    form = UserLoginForm()
    return render(request=request, template_name=template_name, context={"form": form})

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home:index")
