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
        fields = '__all__'

# get sub categories of a category
class GetCategorySubSerializer(ModelSerializer):
    category_name = serializers.ReadOnlyField()
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'category_name')

# create products
class CreateProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# get products under a particular sub category
class SubProductSerializer(ModelSerializer):
    sub_category_name = serializers.ReadOnlyField()
    class Meta:
        model = Product
        fields = ('id', 'name', 'actual_price', 'sales_price', 'first_description', 'second_description', 
                  'sub_category_name', 'date_added', 'product_img')

# create comments
class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ProductCommentSerializer(ModelSerializer):
    product_name = serializers.ReadOnlyField()
    class Meta:
        model = Comment
        fields = ('id', 'comment', 'rate', 'product_name')
