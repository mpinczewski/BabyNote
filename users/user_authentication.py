from django.conf import settings
# from django.contrib.auth import get_user_model
from rest_framework import exceptions
import jwt
from .models import CustomUser


def is_authenticated(token, saved_user):

    token_user_id = token

    print(token_user_id)
    print(saved_user)

    if not token_user_id:
        return None

    if not saved_user:
        return None

    try:
        token_payload = jwt.decode(token_user_id, key=settings.SECRET_KEY, algorithms='HS256')
        
        print('--------------------')
        print(token_payload)

    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Token expired')
    # except IndexError:
    #     raise exceptions.AuthenticationFailed('Token prefix missing')

    user = CustomUser.objects.filter(id=token_payload['user_id']).first()

    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('User is not active')

    return (user, None)