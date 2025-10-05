from django.shortcuts import render, redirect
from memberships.models import MembershipFile
from home.models import ClubFile

def documents(request):
    documents = MembershipFile.objects.all()
    other_documents = ClubFile.objects.all()
    return render(request, "dashboard/documents/index.html", {"documents": documents, "other_docs": other_documents})