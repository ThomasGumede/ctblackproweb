from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from home.utilities.custom_email import send_email_to_admin
from memberships.models import MembershipEmail, MembershipFile
from memberships.forms import MembershipEmailForm
import logging, mimetypes

logger = logging.getLogger("accounts")


def join_membership(request):
    if request.method == 'POST':
        form = MembershipEmailForm(request.POST)
        if form.is_valid():
            recaptcha_token = form.cleaned_data.get('recaptcha_token')
            # print(recaptcha_token)
            try:
                
                form.save()
                send_email_to_admin("Interested In Joining The Club", form.cleaned_data["message"], form.cleaned_data["from_email"], form.cleaned_data["name"])
                messages.success(request, "We have successfully receive your email, will be in touch shortly")
                return redirect("memberships:membership")
            
            except ValueError as e:
                logger.error(f"Failed to verify this due to f{e}")
                messages.success(request, "We have successfully receive your email, will be in touch shortly")
                return redirect("memberships:membership")
            
            
        else:
            messages.error(request, "Something went wrong, please fix errors below")
            for field in form:
                if field.errors:
                    messages.error(request, f"{field.label}: {field.errors.as_text()}")
                return redirect("memberships:membership")
            
    form = MembershipEmailForm()
    
    return render(request, 'membership/join-us.html', {"form": form})

def download_membership_rates(request):
    try:
        membership_rates = MembershipFile.objects.get(slug="membership-rates")
        
        file_path = membership_rates.file.path
        file_name = membership_rates.file.name
        if file_path and file_name:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                mime_type, _ = mimetypes.guess_type(file_path)
                mime_type = mime_type or 'application/octet-stream'
                response = HttpResponse(file_data, content_type=mime_type)
                    
            response['Content-Disposition'] = f'attachment; filename="{file_name.split("/")[-1]}"'
        
        return response
    except MembershipFile.DoesNotExist as er:
        logger.error(f"Something went wrong while downloading the file: {er}")
        messages.error(request, "Membership rates have't been aploaded yet, send us an email for more enquires join@ctblackpros.co.za")
        return redirect("memberships:membership")
    
    except Exception as er:
        logger.error(f"Something went wrong while downloading the file: {er}")
        messages.error(request, "Membership rates have't been aploaded yet, send us an email for more enquires join@ctblackpros.co.za")
        return redirect("memberships:membership")

def download_membership_form(request):
    try:

        membership_join_file = MembershipFile.objects.get(slug="membership-joining-form")
        
        file_path = membership_join_file.file.path
        file_name = membership_join_file.file.name
        if file_path and file_name:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                mime_type, _ = mimetypes.guess_type(file_path)
                mime_type = mime_type or 'application/octet-stream'
                response = HttpResponse(file_data, content_type=mime_type)
                    
            response['Content-Disposition'] = f'attachment; filename="{file_name.split("/")[-1]}"'
        
        return response
    except MembershipFile.DoesNotExist as er:
        logger.error(f"Something went wrong while downloading the file: {er}")
        messages.error(request, "Membership join form has not been aploaded yet, send us an email for more enquires join@ctblackpros.co.za")
        return redirect("memberships:membership")
        
    except Exception as er:
        logger.error(f"Something went wrong while downloading the file: {er}")
        messages.error(request, "Membership join form has not been aploaded yet, send us an email for more enquires join@ctblackpros.co.za")
        return redirect("memberships:membership")