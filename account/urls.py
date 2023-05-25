from django.urls import path, re_path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [

    path('register/', views.register_user, name='register_user'),
    
    path('user/', views.get_update_delete_user, name='get_update_delete_user'),

    path('sign_in/', views.login_user, name='sign_in'),

    re_path(r'^reset_password/', views.ChangePasswordView.as_view(), name='reset_password'),
    re_path(r'^token_refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),

]