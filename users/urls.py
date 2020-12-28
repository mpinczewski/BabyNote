
from django.urls import path
from .views import Users, UserDetails, RegisterUser
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('users/', Users.as_view()),
    path('register/', RegisterUser.as_view()),
    path('user_details/<int:pk>/', UserDetails.as_view()),
    path('login_api/', obtain_auth_token, name="login_api"),
]