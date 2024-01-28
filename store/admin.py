from django.contrib import admin

from .models import Category, Product, Comment, SubCategory, Cart, Favourite, FavItem, Order
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(SubCategory)
admin.site.register(Cart)
admin.site.register(Favourite)
admin.site.register(FavItem)
admin.site.register(Order)
# admin.site.register(Transaction)
