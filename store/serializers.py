from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from account.models import User
from .models import Category, SubCategory, Product, Comment, Cart, ProductItem, FavItem, Favourite, Order, Charge

# create category


class CategorySerializer(serializers.ModelSerializer):
    # sub_category = serializers.PrimaryKeyRelatedField(many=True, queryset=SubCategory.objects.all())
    class Meta:
        model = Category
        fields = ('id', 'name')

# create sub category


class PostSubCategorySerializer(ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=False)

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'category')

# get sub categories of a category


class GetCategorySubSerializer(ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'category_name')

# create comments


class CommentSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=False)
    commenter = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=False)

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'rate', 'commenter', 'product')

# get comments


class GetCommentSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.name')
    commenter = serializers.ReadOnlyField(source='commenter.username')

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'rate', 'commenter', 'product')

# create products


class CreateProductSerializer(ModelSerializer):
    sub_category = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(), many=False)
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'actual_price', 'sales_price', 'desc',
                  'views', 'product_img', 'sub_category', 'comment')


class GetProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCommentSerializer(ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'rate', 'product_name')

# create product item


class ProductItemSerializer(ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all(), many=False)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=False)

    class Meta:
        model = ProductItem
        fields = ('id', 'quantity', 'amount', 'product', 'cart')

# get product item


class GetProductItemSerializer(ModelSerializer):
    product = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = ProductItem
        fields = ('id', 'quantity', 'amount', 'product')


class CartSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True)
    user = serializers.ReadOnlyField(source='user.email')
    total_amount = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ('user', 'product', 'total_amount')


class GetCartSerializer(serializers.ModelSerializer):

    product = CreateProductSerializer(many=True)
    # total_amount = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ('user', 'product', 'total_amount')


class FavItemSerializer(ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=False)
    favourite = serializers.PrimaryKeyRelatedField(
        queryset=Favourite.objects.all(), many=False)

    class Meta:
        model = FavItem
        fields = ('id', 'product', 'favourite')


class GetFavItemSerializer(ModelSerializer):
    product = CreateProductSerializer()
    favourite = serializers.ReadOnlyField(source='favourite.name')

    class Meta:
        model = FavItem
        fields = ('id', 'product', 'favourite')


class FavouriteSerializer(ModelSerializer):
    favourite = GetFavItemSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Favourite
        fields = ('id', 'user', 'favourite')

# create order


class OrderSerializer(ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(), many=False)
    # products = serializers.StringRelatedField(many=True, allow_empty=False)
    products = CreateProductSerializer(many=True)

    class Meta:
        model = Order
        # fields = ('id', 'user', 'first_name', 'last_name', 'phone',
        #           'address', 'state', 'city', 'method', 'status', 'amount')
        fields = ('id', 'first_name', 'last_name', 'products',
                  'phone', 'address', 'state', 'city', 'method', 'status', 'amount')


class GetOrderSerializer(ModelSerializer):
    products = GetProductSerializer(many=True)
    # user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Order
        fields = ('id', 'first_name', 'last_name', 'products',
                  'phone', 'address', 'state', 'city', 'method', 'status', 'amount')

# get all products under a category


class GetCategoryProducts(ModelSerializer):

    sub_category = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(), many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'sub_category')


class AllSubCategorySerializer(serializers.ModelSerializer):
    sub_category = GetCategorySubSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'sub_category')


class ChargeSerializer(ModelSerializer):

    class Meta:
        model = Charge
        fields = '__all__'


class TransferSerializer(serializers.Serializer):
    email = serializers.EmailField()
    amount = serializers.IntegerField()
