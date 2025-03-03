import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import now
from twilio.rest import Client

def home(request):
    return render(request, 'home.html')

def booking(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        date = request.POST['date']
        time = request.POST['time']
        proof = request.FILES['proof']
        
        if int(time.split(':')[0]) < 8 or int(time.split(':')[0]) > 16:
            messages.error(request, "Booking time must be between 8 AM and 4 PM")
            return redirect('booking')

        if int(date.weekday()) == 6:
            messages.error(request, "Bookings are only allowed Monday to Saturday")
            return redirect('booking')

        fs = FileSystemStorage()
        proof_name = fs.save(proof.name, proof)
        
        Booking.objects.create(name=name, phone=phone, date=date, time=time, proof_of_payment=proof_name)
        send_whatsapp_reminder(name, phone, date, time)
        return redirect('success')
    
    return render(request, 'booking.html')

def success(request):
    return render(request, 'success.html')

# WhatsApp Reminder
TWILIO_ACCOUNT_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

def send_whatsapp_reminder(name, phone, date, time):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = f"Hello {name}, your booking at Polished Nailbar is confirmed for {date} at {time}. See you soon!"
    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=message,
        to=f'whatsapp:{phone}'
    ) 