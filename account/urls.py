from django.urls import path, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [

    path('register/', views.register_user, name='register_user'),
    
    path('user/<str:username>/', views.get_update_delete_user, name='get_update_delete_user'),

    re_path(r'^reset_password/', views.ChangePasswordView.as_view(), name='rest_password'),
    re_path(r'^sign_in/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token_refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),

]