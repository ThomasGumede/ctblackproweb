from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Account
from accounts.forms import AccountUpdateForm, GeneralEditForm
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def accounts(request):
    users = Account.objects.all().order_by('created')
    return render(request, "dashboard/users/users.html", {"users": users})

@login_required
def user(request, username):
    user = get_object_or_404(Account, username=username)
    return render(request, "dashboard/users/user.html", {"user": user})

@login_required
def profile(request, username):
    user = get_object_or_404(Account, username=username, id=request.user.id)
    form = AccountUpdateForm(instance=user)
    return render(request, "dashboard/users/profile.html", {"user": user, "form": form})

@login_required
def update_profile(request, username):
    user = get_object_or_404(Account, username=username, id=request.user.id)
    if request.method == "POST":
        form = AccountUpdateForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile details updated successfully")
        else:
            messages.error(request, "Unable to update profile details")
    
    
    return redirect("dashboard:profile-details", user.username)



@login_required
def update_profile_password(request, username):
    
    user = get_object_or_404(Account, username=username, id=request.user.id)
    form = PasswordChangeForm(user)
    if request.method == "POST":
        form = PasswordChangeForm(user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile password updated successfully")
        else:
            messages.error(request, "Unable to update your password, try again")
    
    return redirect("dashboard:profile-details", user.username)

@login_required
def delete_user(request, username):
    user = get_object_or_404(Account, username=username)
    return render(request, "dashboard/users/delete-user.html", {"user": user})