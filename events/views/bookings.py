from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from events.forms import BookingForm
from events.models import Event, Booking
from events.utilities.choices import StatusChoices
from events.utilities.file_handlers import generate_booking_number

@login_required
def confirm_attendance(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)

    if not event.is_open:
        messages.error(request, "Bookings for this game are closed.")
        return redirect("events:event-details", event_slug=event.slug)

    application = Booking.objects.filter(event=event, user=request.user).first()
    
    if application:
        if application.payment_status == "cancelled" or application.payment_status == "Not Completed":
            application.delete()
        else:
            messages.info(request, "You've already confirmed attendance for this event.")
            return redirect("events:booking-success", application.payment_referrence)

    if event.available_slots <= 0:
        messages.error(request, "Sorry, this event is fully booked.")
        return redirect("events:event-details", event_slug=event.slug)

    booking = Booking.objects.create(event=event, user=request.user, payment_referrence=generate_booking_number(Booking))
    messages.success(request, "Attendance confirmed! Proceed to payment.")
    return redirect("events:booking-payment", booking_id=booking.id)

@login_required
def booking_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    event = booking.event
    total_cost = booking.calculate_total_cost()
    form = BookingForm(instance=booking)
    if request.method == "POST":
        form = BookingForm(data=request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.total_cost = booking.calculate_total_cost()
            booking.payment_status = StatusChoices.PENDING
            booking.save(update_fields=["billing_name", "billing_surname", "billing_email", "billing_phone", "billing_address", "company_name", "company_address", "booking_note", "payment_method","total_cost", "payment_status"])

            if booking.payment_method == "Yoco":
                messages.warning(request, "Yoco payment gateway is currently unavailable.")
            else:
                messages.success(request, f"Booking successful! Total cost: R{booking.total_cost}")
                
            return redirect("events:booking-success", booking.payment_referrence)
        else:
            messages.error(request, "Something Went wrong, fix errors below")
        
    context = {"booking": booking, "event": event, "total_cost": total_cost, "form": form}
    return render(request, "events/bookings/checkout.html", context)


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking_id = booking.payment_referrence
    booking.delete()
    messages.success(request, f"Booking number {booking_id} Was Cancelled successfully")
    return redirect("home:index")

@login_required
def booking_success(request, payment_referrence):
    booking = get_object_or_404(Booking, payment_referrence=payment_referrence, user=request.user)
    return render(request, "events/bookings/booking-confirm.html", {"booking": booking})