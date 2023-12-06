from django.db import models

from accounts.models import CustomUser
from store.models import Variation

# Create your models here.
class WishlistItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Variation,on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username}'s Wishlist - {self.product_name}"