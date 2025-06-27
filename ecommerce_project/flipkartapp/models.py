# flipkartapp/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='Products/', blank=True, null=True)  # ← Add this

    def __str__(self):
        return self.name

# flipkartapp/models.py
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('skincare', 'Skincare'),
        ('makeup', 'Makeup'),
        ('haircare', 'Haircare'),
        ('fragrance', 'Fragrance'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='Products/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')  # ← new
    rating = models.FloatField(default=4.0)  #

    def __str__(self):
        return self.name
