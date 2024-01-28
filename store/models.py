from django.db import models
from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


def default_policy():
    try:
        return Category.objects.get(name="Uncategorized").pk
    except Category.DoesNotExist:
        try:
            Category.objects.create(name="Uncategorized")
        except:
            pass


def default_sub():
    try:
        return SubCategory.objects.get(name="Uncategorized").pk
    except SubCategory.DoesNotExist:
        try:
            SubCategory.objects.create(name="Uncategorized")
        except:
            pass


def default_product():
    try:
        return Product.objects.get(name="Uncategorized").pk
    except Product.DoesNotExist:
        try:
            Product.objects.create(name="Uncategorized")
        except:
            pass


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, related_name='sub_category', on_delete=models.PROTECT, db_constraint=False)
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
    sales_price = models.IntegerField(
        null=True, blank=True, default=0)  # might go off
    desc = models.TextField()
    sub_category = models.ForeignKey(
        SubCategory, related_name='product', on_delete=models.PROTECT, db_constraint=False)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='product', blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='product', blank=True, null=True
    )
    views = models.IntegerField(blank=True, null=True, default=0)
    product_img = models.ImageField(upload_to=upload_to, blank=True, null=True)
    # cart = models.ForeignKey(
    #     Cart, on_delete=models.CASCADE, related_name='product', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    @property
    def sub_category_name(self):
        return self.sub_category.name

    # get rating
    @property
    def get_rating(self):
        rating = 0
        count = 0
        for i in self.comment:
            rating += i.rate
            count += 1
        rating = rating / count
        return rating

    # get comments


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='cart')
    total_amount = models.IntegerField(default=0, blank=True, null=True)
    products = models.ManyToManyField(Product, related_name="cart_products")
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.email}'s cart"


class Comment(models.Model):
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment')
    product = models.ForeignKey(
        Product, related_name='comment', on_delete=models.PROTECT, db_constraint=False)
    comment = models.TextField()
    rate = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.comment[:20]

    @property
    def product_name(self):
        return self.product.name


# class ProductItem(models.Model):
#     product = models.ForeignKey(
#         Product, on_delete=models.CASCADE, related_name='product_item')
#     quantity = models.IntegerField()
#     amount = models.IntegerField(null=True, blank=True)
#     cart = models.ForeignKey(
#         Cart, on_delete=models.CASCADE, related_name='product_item')
#     date_added = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return f"{self.cart.user.email}'s product item - {self.product.name}"


class Favourite(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='favourite')
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.email}'s favourite"


class FavItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product')
    favourite = models.ForeignKey(
        Favourite, on_delete=models.CASCADE, related_name='favourite')
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.favourite.user.email}'s favourite item"


# class Transaction(models.Model):
#     status = models.CharField(max_length=40)
#     transaction_ref = models.CharField(max_length=100)
#     amount = models.IntegerField()
#     payment_type = models.CharField(max_length=30)
#     customer_email = models.EmailField()
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return f'{self.customer_email} - {self.event}'
