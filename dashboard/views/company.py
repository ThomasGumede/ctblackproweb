from django.shortcuts import render, redirect
from memberships.models import MembershipFile
from home.models import ClubFile
from accounts.models import Company

def company(request):
    company = Company.objects.first()
    
    return render(request, "dashboard/company/index.html", {"company": company})