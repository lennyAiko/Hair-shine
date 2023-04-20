from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Category, SubCategory, Product, Rating, Comment

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
    category = CategorySerializer()
    class Meta:
        model = SubCategory
        fields = ('name', 'category')

# get sub categories of a category
class GetCategorySubSerializer(serializers.Serializer):
    name = PostSubCategorySerializer()

# create products
class CreateProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ['views']