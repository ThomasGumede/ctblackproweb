import uuid, re
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

def handle_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"post/{filename}"

def generate_application_number(model) -> str:
    application_id_start = f'CTB-{timezone.now().year}{timezone.now().month}'
    queryset = model.objects.filter(application_number__iexact=application_id_start).count()
      
    count = 1
    application_number = application_id_start
    while(queryset):
        application_number = f'CTB-{timezone.now().year}{timezone.now().month}{count}'
        count += 1
        queryset = model.objects.all().filter(application_number__iexact=application_number).count()

    return application_number