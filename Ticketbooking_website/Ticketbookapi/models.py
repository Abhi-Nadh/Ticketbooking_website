from django.db import models
from django.contrib.auth.models import User

class Booking_models(models.Model):
    user_id=models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    movie_id=models.ForeignKey("admin_show_site.Movie_details",on_delete=models.CASCADE)
    seat=models.CharField(null=True,max_length=50)
    price=models.FloatField(null=True)
    count=models.IntegerField()
    total_price=models.FloatField(null=True)

class Payment_status(models.Model):
    customer_details = models.ForeignKey("Booking_models",on_delete=models.CASCADE)
    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=200,null=True,default = None)
    payment_signature = models.CharField(max_length=200,null=True,default = None)
    # payment_complete = models.IntegerField(default = 0)
    paydone = models.DateTimeField(auto_now_add=True)
    
    