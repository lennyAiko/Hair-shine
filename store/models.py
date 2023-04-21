from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')
    name = models.CharField(max_length=150, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.category.name}'
    
    @property
    def category_name(self):
        return self.category.name
    
class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    actual_price = models.IntegerField(default=0)
    sales_price = models.IntegerField(null=True, blank=True, default=0)
    first_description = models.TextField()
    second_description = models.TextField()
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    views = models.IntegerField(blank=True, null=True, default=0)
    product_img = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    # get rating

    # get comments

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField()
    rate = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )