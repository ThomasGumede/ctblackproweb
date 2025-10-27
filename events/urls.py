from events.views.event import event_details, events
from events.views.bookings import confirm_attendance, booking_payment, booking_success, cancel_booking
from django.urls import path

app_name = "events"
urlpatterns = [
    path('events', events, name='events'), 
    path('event/<event_slug>', event_details, name='event-details'),
    path('event/<event_slug>/booking', confirm_attendance, name='booking'),
    path('event/<booking_id>/booking-confirmation', booking_payment, name='booking-payment'),
    path('event/<booking_id>/cancel-booking', cancel_booking, name='cancel-booking'),
    path('event/<payment_referrence>/booking-success', booking_success, name='booking-success'),
]


# Create your views here.
