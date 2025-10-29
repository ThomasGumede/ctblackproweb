from django.shortcuts import redirect
from django.contrib import messages

def restrict_for_captain(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.role in ["Captain", "Chairman"]:
            messages.error(request, "Only Captains can add events")
            return redirect("dashboard:events")
        
        return view_func(request, *args, **kwargs)
        
    return wrapper