# from django.core import exceptions
from .models import CustomUser, Profile
from .serializers import ProfileSerializer, UserSerializer, RegistrationSerializer

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView, exceptions

from .utils.generate_token import get_token
from .utils.user_authentication import authenticate_user, get_profile, get_profile_id


class LoginView(APIView):
    def get(self, request):
        response = {"request": request.data}

        return Response(response)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                "Email and Password must be provided."
            )

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed("User not found.")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Wrong Password.")

        token = get_token(user)

        return Response({"token": token})


class Users(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUser(generics.CreateAPIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data["response"] = "Registered new user."
            data["email"] = account.email
            profile_email = request.POST.get('email')
            user = CustomUser.objects.get(email=profile_email)
            profile = Profile(user=user)
            profile.save()

        else:
            data = serializer.errors

        return Response(data, status.HTTP_201_CREATED)

class UserDetails(generics.ListCreateAPIView):
    def get(self, request):
        token_user = authenticate_user(request)
        serializer = UserSerializer(token_user)

        return Response(serializer.data)

    def patch(self, request):
        token_user = authenticate_user(request)
        serializer = UserSerializer(token_user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetails(generics.RetrieveUpdateAPIView):
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=get_profile_id(self.request))
        obj = generics.get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)

        return obj

    def get(self, request):
        profile_data = get_profile(request)
        serializer = ProfileSerializer(profile_data)

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


   