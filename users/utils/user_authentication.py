from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import exceptions
from ..models import Profile
from django.http import HttpResponse
from rest_framework import status


def authenticate_user(request):
    """
    weryfikacja poprawności przekazanego tokena
    """
    try:
        return JWTAuthentication().authenticate(request)[0]
        """return User instance"""

    except:
        raise exceptions.AuthenticationFailed("Bad token")

def get_profile(request):
    """
    wyciągam z tokena przekazanego requestem obiekt usera
    """
    try:
        token_user = authenticate_user(request)
        return Profile.objects.get(user=token_user)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

def get_profile_id(request):

    """
    wyciągam z tokena przekazanego requestem id usera
    """

    try:
        token_user = authenticate_user(request)
        return Profile.objects.get(user=token_user).id
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)