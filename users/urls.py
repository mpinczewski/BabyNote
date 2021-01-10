
from django.urls import path, include
from .views import Users, UserDetails, RegisterUser, LoginView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('users/', Users.as_view(), name='users'),
    path('register/', RegisterUser.as_view(), name="register"),
    path('user_details/<int:pk>/', UserDetails.as_view()),

# restframework_simplejwt
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenObtainPairView.as_view()),

# allauth
    path('accounts/', include('allauth.urls')),
    path('login/', LoginView.as_view(), name="login"),
]