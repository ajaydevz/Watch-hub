from django.db import models

from accounts.models import CustomUser
# Create your models here.


class Address(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    house_no = models.IntegerField()
    recipient_name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=50)
    village_name = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"Adress for {self.recipient_name}"
    
    