from django.db import models
from django.urls import reverse
from categories.models import Category, Sub_Category


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        Sub_Category, on_delete=models.CASCADE, default=None
    )
    created_date = models.DateField(auto_now_add=True)
    modified_data = models.DateField(auto_now=True)
    is_activate = models.BooleanField(default=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    # def get_url(self):
    #     return reverse('product_detail', args=[self.category.slug, self.slug])

    def _str_(self):
        return self.product_name

    class Meta:
        verbose_name = "variation"
        verbose_name_plural = "variations"

    def _str_(self):
        return f"{self.product.product_name} - {self.color}"


class Variation(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variations"
    )
    color = models.CharField(max_length=20)
    stock = models.PositiveIntegerField(default=0)  # Use PositiveIntegerField for stock
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=None
    )  # Use DecimalField for precise pricing
    actual_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=None
    )
    is_available = models.BooleanField(default=True)
    image1 = models.ImageField(upload_to="photos/products/", default=None)
    image2 = models.ImageField(upload_to="photos/products/", default=None)
    image3 = models.ImageField(upload_to="photos/products/", default=None)
    image4 = models.ImageField(upload_to="photos/products/", default=None)

    class Meta:
        verbose_name = "variation"
        verbose_name_plural = "variations"

    def _str_(self):
        return f"{self.product.product_name} - {self.color}"


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=20, default="discount coupon")
    code = models.CharField(max_length=10)
    discount = models.IntegerField(default=100)
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_expired = models.BooleanField(default=False)
    minimum_amount = models.IntegerField(default=500)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.code
