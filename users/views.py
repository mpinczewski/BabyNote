from django.core import exceptions
from django.shortcuts import render
from django.http import HttpResponse, response
from .models import CustomUser, TempJWTToken
from .serializers import UserSerializer, RegistrationSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.backends import TokenBackend

from .generate_token import generate_access_token, generate_refresh_token

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

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        token_data = TempJWTToken(refresh=refresh_token, access=access_token)
        token_data.save()

        return Response({'Poszło': 'zapisane w bazie danych', 'access_token': access_token})

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

    def get(self, request, pk):

        saved_user = self.get_object(pk)
        token = request.headers.get('Authorization')
        logged_user = is_authenticated(token, saved_user)

        serializer = UserSerializer(saved_user)

        if not logged_user:
            return Response({'response': 'brak uprawnien(token nie został przekazany)'})

        if saved_user != logged_user:
            return Response({'response': 'brak uprawnien'})
        
        return Response(serializer.data)

    def put(self, request, pk):

        saved_user = self.get_object(pk)
        serializer = UserSerializer(saved_user, data=request.data)
        logged_user = request.user

        if saved_user != logged_user:
            return Response({'response': 'brak uprawnien'})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

