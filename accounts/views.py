from datetime import timedelta

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import CodeForm, EmailForm, OnboardingForm
from .models import LoginCode, User


def request_code(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = EmailForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        blocked = User.objects.filter(email=email, is_blocked=True).exists()
        too_soon = LoginCode.objects.filter(
            email=email, created_at__gt=timezone.now() - timedelta(seconds=60)
        ).exists()
        if blocked:
            form.add_error("email", "This email can't be used to sign in.")
        elif too_soon:
            form.add_error("email", "A code was just sent. Wait a minute and try again.")
        else:
            code = LoginCode.issue(email)
            send_mail(
                "Your sign-in code",
                f"Your code is {code}. It expires in 10 minutes.",
                None,
                [email],
            )
            request.session["login_email"] = email
            return redirect("accounts:verify")
    return render(request, "accounts/form.html", {"title": "Sign in", "form": form, "button": "Send code"})


def verify_code(request):
    email = request.session.get("login_email")
    if not email:
        return redirect("accounts:login")
    form = CodeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login_code = LoginCode.objects.filter(email=email, used=False).order_by("-created_at").first()
        if login_code and login_code.is_valid() and login_code.verify(form.cleaned_data["code"]):
            login_code.used = True
            login_code.save(update_fields=["used"])
            user = User.objects.filter(email=email).first() or User.objects.create_user(email=email)
            if user.is_blocked or not user.is_active:
                form.add_error("code", "This email can't be used to sign in.")
            else:
                login(request, user)
                request.session.pop("login_email", None)
                return redirect("home" if user.name else "accounts:onboarding")
        else:
            form.add_error("code", "That code is wrong or expired. Go back and request a new one.")
    return render(request, "accounts/form.html", {"title": "Enter your code", "form": form, "button": "Sign in"})


@login_required
def onboarding(request):
    if request.user.name:
        return redirect("home")
    form = OnboardingForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("home")
    return render(request, "accounts/form.html", {"title": "Tell us about you", "form": form, "button": "Continue"})