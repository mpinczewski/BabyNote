# from django.core import exceptions
from django.http import HttpResponse, response
from .models import CustomUser
from .serializers import UserSerializer, RegistrationSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView, exceptions

from .generate_token import get_token

from .user_authentication import is_authenticated

class LoginView(APIView):
    def get(self, request):

        response = {'request': request.data}

        return Response(response)

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed('Email and Password must be provided.')

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found.')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Wrong Password.')

        token = get_token(user)

        return Response({'token': token})


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


class RegisterUser(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = "Registered new user."
            data['email'] = account.email

        else:
            data = serializer.errors

        return Response(data, status.HTTP_201_CREATED)


class UserDetails(APIView):

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)

        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def authorize_user(self, request, pk):

        saved_user = self.get_object(pk)
        logged_user = is_authenticated(request, saved_user)
        return logged_user

    def get(self, request, pk):

        authorize_user = self.authorize_user(request, pk)
        serializer = UserSerializer(authorize_user)

        return Response(serializer.data)

    def put(self, request, pk):

        authorize_user = self.authorize_user(request, pk)
        serializer = UserSerializer(authorize_user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


