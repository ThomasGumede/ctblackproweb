from django.utils import timezone
import uuid

def handle_event_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"event/{filename}"

def generate_booking_number(model) -> str:
    booking_id_start = f'CTB-P{timezone.now().year}{timezone.now().month}'
    queryset = model.objects.filter(payment_referrence__iexact=booking_id_start).count()
      
    count = 1
    booking_number = booking_id_start
    while(queryset):
        booking_number = f'CTB-P{timezone.now().year}{timezone.now().month}{count}'
        count += 1
        queryset = model.objects.all().filter(payment_referrence__iexact=booking_number).count()

    return booking_number