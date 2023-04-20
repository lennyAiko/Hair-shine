from django.urls import path, re_path

from .views import category, sub_category, product

urlpatterns = [

    # categories
    path('categories/', category.create_get),
    path('categories/<int:id>/', category.get_update_delete),
    path('categories/<int:id>/subs', category.get_subs),

    # sub categories
    path('sub_categories/', sub_category.create),
    path('sub_categories/<int:id>', sub_category.get_subcategories),
    # path('sub_categories/<int:id>', category.get_update_delete, name='categories'),

    # products
    path('products/', product.create_get),
]