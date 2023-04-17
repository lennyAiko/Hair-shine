from django.urls import path, re_path

from .views import category, sub_category

urlpatterns = [

    path('categories/', category.create_get, name='categories'),
    path('categories/<int:id>', category.get_update_delete, name='categories'),

    path('sub_categories/', sub_category.create_get, name='sub_categories'),
    # path('sub_categories/<int:id>', sub_category.create_get, name='sub_categories'),
    # path('sub_categories/<int:id>', category.get_update_delete, name='categories'),
]