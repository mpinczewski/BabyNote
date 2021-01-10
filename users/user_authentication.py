from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import exceptions

def is_authenticated(request, saved_user):
    
    jwt_object      = JWTAuthentication() 
    header          = jwt_object.get_header(request)
    raw_token       = jwt_object.get_raw_token(header)
    validated_token = jwt_object.get_validated_token(raw_token)
    user            = jwt_object.get_user(validated_token)
    print(user)
    print(saved_user)


# nie działa weryfikacja sprawdzająca czy user z tokena jest w bazie!!!
    if not saved_user:
        raise exceptions.AuthenticationFailed('No user database')

    if user is None:
        raise exceptions.AuthenticationFailed('No user data provided')

    if user != saved_user:
        raise exceptions.AuthenticationFailed('Wrong user')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('User is inactive')

    return (saved_user)


    