from django.shortcuts import redirect, render, get_object_or_404
from home.models import ClubFile
from django.http import HttpResponse
from django.contrib import messages
import logging, mimetypes

logger = logging.getLogger("home")

def get_club_files(request):
    club_files = ClubFile.objects.all()
    return render(request, 'club/files.html', {"files": club_files})

def download_file(request, file_id):
    media = get_object_or_404(ClubFile.objects.all(), id=file_id)
    
    try:
            file_path = media.mediafile.path
            file_name = media.mediafile.name
            if file_path and file_name:
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    mime_type, _ = mimetypes.guess_type(file_path)
                    mime_type = mime_type or 'application/octet-stream'
                    response = HttpResponse(file_data, content_type=mime_type)
                    
                response['Content-Disposition'] = f'attachment; filename="{file_name.split("/")[-1]}"'
        
            return response
    except Exception as ex:
        logger.error("Missing Media file")
        messages.error(request, "Media file not aploaded yet, send us an email if you have questions")
        return redirect("goldours_home:media-details", file_id=media.id)