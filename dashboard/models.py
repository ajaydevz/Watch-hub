from django.db import models
from image_cropping import ImageCropField, ImageRatioField


# Create your models here.
class Banner(models.Model):
    banner_name = models.CharField(max_length=50)
    banner_image = models.ImageField(upload_to="photos/banner/", default=None)
    banner_count = models.IntegerField(default=1)

    def __str__(self):
        return self.banner_name
