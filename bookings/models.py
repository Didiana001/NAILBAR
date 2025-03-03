from django.db import models
class Booking(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    proof_of_payment = models.ImageField(upload_to='payments/')
    created_at = models.DateTimeField(auto_now_add=True)
