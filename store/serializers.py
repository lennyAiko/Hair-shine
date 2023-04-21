from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Category, SubCategory, Product, Comment

# create category
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# create sub category
class PostSubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('name', 'category')

# get sub categories and the category they belong
class GetSubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('name', 'category')

# get sub categories of a category
class GetCategorySubSerializer(ModelSerializer):
    category_name = serializers.ReadOnlyField()
    class Meta:
        model = SubCategory
        fields = ('name', 'category_name')

# create products
class CreateProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ['views']

# get products under a particular sub category
class SubProductSerializer(ModelSerializer):
    product = CreateProductSerializer()
    class Meta:
        model = SubCategory
        fields = ('name', 'product')