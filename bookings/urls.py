from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('booking/', booking, name='booking'),
    path('success/', success, name='success'),
]
# Compare this snippet from polished_nailbar/bookings/models.py: