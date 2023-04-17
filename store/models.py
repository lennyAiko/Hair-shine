from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.category.name}'
    
class Product(models.Model):
    name = models.CharField(max_length=150)
    actual_price = models.DecimalField(max_digits=9, decimal_places=2)
    sales_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    first_description = models.TextField()
    second_description = models.TextField()
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    views = models.IntegerField()

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    ) # always set a range

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()