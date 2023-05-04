from django.urls import path, re_path

from .views import category, sub_category, product, comments, cart, order, favourites

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
    # path('products/', product.ProductList.as_view()),
    path('products/', product.create_get),
    path('products/<int:index>/', product.get_update_delete),
    path('products/<int:index>/comments/', product.get_comments),
    path('products/new/', product.new_products),
    path('products/trending/', product.trending_products),

    #comments
    path('comments/', comments.create_get),
    path('comments/<int:index>/', comments.get_update_delete),

    #cart
    path('cart/', cart.get),
    path('cart/items/', cart.add_item),
    path('cart/items/<int:index>/', cart.get_update_delete_item),
    path('cart/empty/', cart.empty_cart),

    #order
    path('orders/all/', order.get_all),
    path('orders/', order.create_get),
    path('orders/<int:index>/', order.get_update_delete_item),

    #favorites
    path('favourite/', favourites.get),
    path('favourite/items/', favourites.add_item),
    path('favourite/items/<int:index>/', favourites.get_update_delete_item)

]