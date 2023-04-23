from django.urls import path, re_path

from .views import category, sub_category, product, comments

urlpatterns = [

    # categories
    path('categories/', category.create_get),
    path('categories/<int:id>/', category.get_update_delete),
    path('categories/<int:id>/subs/', category.get_subs),

    # sub categories
    path('sub_categories/', sub_category.create_get),
    path('sub_categories/<int:id>/products/', sub_category.get_products),
    path('sub_categories/<int:id>/', sub_category.get_update_delete),

    # products
    path('products/', product.create_get),
    path('products/<int:id>/', product.get_update_delete),
    path('products/<int:id>/comments/', product.get_comments),
    
    #comments
    path('comments/', comments.create_get),
    path('comments/<int:id>/', comments.get_update_delete),

]