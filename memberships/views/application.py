from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from home.utilities.custom_email import send_email_to_admin
from memberships.models import MembershipApplication, MemberAppChoices
from memberships.forms import ApplicationForm, TraceApplicationForm
import logging
from memberships.utilities.decorators import restrict_approved_members
from memberships.utilities.handle_file import generate_application_number

logger = logging.getLogger("accounts")

def pricing(request):
    return render(request, "membership/pricing.html")


def join_membership(request):
    return render(request, 'membership/join-us.html')

@login_required
@restrict_approved_members
def apply_for_membership(request, application_number=None):
    application = None
    if application_number:
        application = get_object_or_404(MembershipApplication, application_number=application_number, user=request.user)
      
    application_form = ApplicationForm(instance=request.user)
    if request.method == 'POST':
        form = ApplicationForm(instance=request.user, data=request.POST)
        if form.is_valid() and form.is_multipart():
            app_number = generate_application_number(MembershipApplication)
            try:
                form.save()
                request.user.membership_number = app_number
                request.user.save(update_fields=["membership_number"])
                
                if application is None:
                    application = MembershipApplication.objects.create(user=request.user, application_number=app_number, status=MemberAppChoices.PENDING)
                
                send_email_to_admin("Interested In Joining The Club", "Kindly Review The Application Below", form.cleaned_data["email"], form.cleaned_data["first_name"])
                messages.success(request, "We have successfully receive your application, will be in touch shortly")
                return redirect("memberships:application-done", application_id=application.id)
            
            except ValueError as e:
                logger.error(f"Failed to verify this due to f{e}")
                messages.success(request, "We have successfully receive your application, will be in touch shortly")
                return redirect("memberships:application-done", application_id=application.id)
            
        else:
            messages.error(request, "Something went wrong, please fix errors below")
            return render(request, 'membership/create-application.html', {"form": form})
    
    if application:
        messages.info(request, f"Please note that you currently have an existing application({application.application_number}) and you are currently updating this application.")       
    return render(request, 'membership/create-application.html', {"form": application_form})

@login_required
def application_submitted(request, application_id):
    application = get_object_or_404(MembershipApplication, id=application_id, user=request.user)
    return render(request, 'membership/application-done.html', {"application": application})

def trace_application(request):
    form = TraceApplicationForm()
    if request.method == 'POST':
        form = TraceApplicationForm(request.POST)
        application = None
        if form.is_valid():
            app_no = form.cleaned_data.get("application_number")
            applicant_email = form.cleaned_data.get("email")
            try:
                application = MembershipApplication.objects.select_related("user").get(application_number=app_no, user__email__iexact=applicant_email)
                return render(request, "membership/trace-application.html", {"form": form, "application": application})
            
            except MembershipApplication.DoesNotExist as ex:
                messages.error(request,"No Application Found For This Number and Email.")
        else:
            messages.error(request, "Please fill both application number and email to trace your application")
            
    return render(request, "membership/trace-application.html", {"form": form})
