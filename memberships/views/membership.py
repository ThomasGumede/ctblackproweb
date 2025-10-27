from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from home.utilities.custom_email import send_email_to_admin
from memberships.models import MembershipEmail, MembershipFile, MembershipApplication
import logging, mimetypes

logger = logging.getLogger("accounts")

def download_files(request, file_slug):
    media = get_object_or_404(MembershipFile, slug=file_slug)
    
    try:
            file_path = media.file.path
            file_name = media.file.name
            if file_path and file_name:
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    mime_type, _ = mimetypes.guess_type(file_path)
                    mime_type = mime_type or 'application/octet-stream'
                    response = HttpResponse(file_data, content_type=mime_type)
                    
                response['Content-Disposition'] = f'attachment; filename="{file_name.split("/")[-1]}"'
        
            return response
    except MembershipFile.DoesNotExist as ex:
        logger.error(f"Missing Media file: {ex}")
        messages.error(request, "Media file not aploaded yet, send us an email if you have questions")
        return redirect("dashboard:documents")
    
    except Exception as ex:
        logger.error(f"Missing Media file: {ex}")
        messages.error(request, "Media file not aploaded yet, send us an email if you have questions")
        return redirect("dashboard:documents")
    
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