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
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, 
                                 related_name='sub_category', default="Uncategorized")
    name = models.CharField(max_length=150, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    @property
    def category_name(self):
        return self.category.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    actual_price = models.IntegerField(default=0)
    sales_price = models.IntegerField(null=True, blank=True, default=0)
    first_description = models.TextField()
    second_description = models.TextField()
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_DEFAULT, related_name='product', default="Uncategorized")
    views = models.IntegerField(blank=True, null=True, default=0)
    product_img = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    
    @property
    def sub_category_name(self):
        return self.sub_category.name

    # get rating
    @property
    def get_rate(self):
        return self.comment.rate

    # get comments

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.SET_DEFAULT, related_name='comment', default="Uncategorized")
    product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, related_name='comment', default="Uncategorized")
    comment = models.TextField()
    rate = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )

    def __str__(self) -> str:
        return self.comment[:20]
    
    @property
    def product_name(self):
        return self.product.name