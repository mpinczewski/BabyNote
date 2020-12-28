from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser
from .serializers import UserSerializer, RegistrationSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login

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

# generuje token przy rejestracji
            token = Token.objects.create(user=account)

            data['response'] = "Registered new user."
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token

        else:
            data = serializer.errors
        
        return Response(data)


class UserDetails(APIView):

    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        
        logged_user = self.get_object(pk)
        serializer = UserSerializer(logged_user)
        saved_user = request.user

        if saved_user != logged_user:
            return Response({'response': 'brak uprawnien'})
        
        return Response(serializer.data)

    def put(self, request, pk):

        logged_user = self.get_object(pk)
        serializer = UserSerializer(logged_user, data=request.data)
        saved_user = request.user

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

