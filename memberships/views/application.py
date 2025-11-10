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

def apply_for_membership(request, application_number=None):
    application = None
    if application_number:
        application = get_object_or_404(MembershipApplication, application_number=application_number)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            
            if not application:
                app_number = generate_application_number(MembershipApplication)
                application = form.save(commit=False)
                application.application_number = app_number
                application.status = MemberAppChoices.PENDING
                application.save()
            else:
                form.save()

            messages.success(request, f"We have successfully received your application ({application.application_number}). You will be contacted shortly.")
            return redirect("memberships:application-done", application_number=application.application_number)
        else:
            messages.error(request, "Something went wrong, please fix errors below.")
    else:
        form = ApplicationForm(instance=application)

    if application:
        messages.info(request, f"You currently have an existing application ({application.application_number}) and you are updating it.")

    return render(request, 'membership/create-application.html', {"form": form})

def application_submitted(request, application_number):
    application = get_object_or_404(MembershipApplication, application_number=application_number)
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
                application = MembershipApplication.objects.get(application_number=app_no, email__iexact=applicant_email)
                return render(request, "membership/trace-application.html", {"form": form, "application": application})
            
            except MembershipApplication.DoesNotExist as ex:
                messages.error(request,"No Application Found For This Number and Email.")
        else:
            messages.error(request, "Please fill both application number and email to trace your application")
            
    return render(request, "membership/trace-application.html", {"form": form})
