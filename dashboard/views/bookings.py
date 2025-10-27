from events.models import Booking
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "dashboard/bookings/bookings.html", {"bookings": bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Your booking was canceled successfully. Thank you")
    return redirect("dashboard:bookings")
