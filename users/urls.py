
from django.urls import path
from .views import Users, UserDetails, RegisterUser


urlpatterns = [
    path('users/', Users.as_view()),
    path('register/', RegisterUser.as_view()),
    path('user_details/<int:pk>/', UserDetails.as_view()),
]