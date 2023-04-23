from django.urls import path, re_path

from .views import category, sub_category, product, comments

urlpatterns = [

    # categories
    path('categories/', category.create_get),
    path('categories/<int:index>/', category.get_update_delete),
    path('categories/<int:index>/subs/', category.get_subs),

    # sub categories
    path('sub_categories/', sub_category.create_get),
    path('sub_categories/<int:index>/products/', sub_category.get_products),
    path('sub_categories/<int:index>/', sub_category.get_update_delete),

    # products
    path('products/', product.create_get),
    path('products/<int:index>/', product.get_update_delete),
    path('products/<int:index>/comments/', product.get_comments),
    path('products/new/', product.new_products),
    path('products/trending/', product.trending_products),

    #comments
    path('comments/', comments.create_get),
    path('comments/<int:index>/', comments.get_update_delete),

]