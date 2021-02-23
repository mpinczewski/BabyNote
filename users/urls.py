from django.urls import path, include
from .views import BabiesList, BabyDetails, ProfileDetails, Users, UserDetails, RegisterUser, LoginView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register"),
    path("user_details/", UserDetails.as_view(), name="user_details"),
    path("profile/", ProfileDetails.as_view(), name="profile"),

    path("baby/<pk>", BabyDetails.as_view(), name="baby"),
    path("baby/list/", BabiesList.as_view(), name="baby_list"),

    # restframework_simplejwt
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh", TokenObtainPairView.as_view()),
    path("login/", LoginView.as_view(), name="login"),
    # allauth
    path("accounts/", include("allauth.urls")),
]
