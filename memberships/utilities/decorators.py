from django.shortcuts import redirect
from django.contrib import messages
from memberships.models import MemberAppChoices, MembershipApplication

def restrict_approved_members(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            membership_app = MembershipApplication.objects.filter(user=user).first()
            if membership_app:
                if membership_app.status == MemberAppChoices.APPROVED:
                    messages.info(request, "You are already an approved member. You cannot access this page")
                    return redirect("memberships:trace-application")
                if membership_app.status == MemberAppChoices.PENDING:
                    messages.info(request, "You already have a PENDING application. Trace your application for progress")
                    return redirect("memberships:trace-application")
                if membership_app.status == MemberAppChoices.COMPLETED:
                    messages.info(request, "Please pay our membership rates for your application. Trace your application for progress")
                    return redirect("memberships:trace-application")
                else:
                    membership_app.delete()
            return view_func(request, *args, **kwargs)
        
    return wrapper

