# from django.core import exceptions
from .models import CustomUser, Profile, Baby
from .serializers import BabySerializer, ProfileSerializer, UserSerializer, RegistrationSerializer

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView, exceptions

from django.http import HttpResponse

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
            profile_id = account.id
            Profile.objects.create(user_id=profile_id)

        else:
            data = serializer.errors

        return Response(serializer.data, status.HTTP_201_CREATED)

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

class BabiesList(generics.ListCreateAPIView):

    def get_data(self, request):

        """
        pobieram request, wyciągam z niego dane i tworzę nowy słownik do którego dodaje dodatkowo
        id profilu

        do sprawdzenia jak zabezpieczyć bazę przed wprowadzeniem złośliwych komend!!!!
        """
        
        data = {
            "profile": get_profile_id(request),
            "baby_name": request.data['baby_name'],
            "baby_birth": request.data['baby_birth'],
            "baby_gender": request.data['baby_gender'],
            "baby_weight": request.data['baby_weight'],
            "baby_height":  request.data['baby_height'],
        }

        return data

    def get_babies(self):
        return Baby.objects.filter(profile_id = get_profile_id(self.request))

    def get(self, request):
        serializer = BabySerializer(self.get_babies(), many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = BabySerializer(data=self.get_data(request))

        if serializer.is_valid():
            serializer.create_baby()
            return Response(serializer.data, status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        

class BabyDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Baby.objects.all()
    serializer_class = BabySerializer

    def get_baby(self, pk):
        """
        Wyciągam z bazy danych dziecko z odpowiednim ID oraz odpowiednim właścicielem. 
        Sprawdzam czy rekord istnieje.

        """
        baby = Baby.objects.filter(
            id = pk, 
            profile = get_profile_id(self.request)
            ).exists()
        
        if baby:
            return Baby.objects.get(
                id = pk, 
                profile = get_profile_id(self.request)
                )
        else:
            raise exceptions.ValidationError("No such baby")

    def get(self, request, pk):
        baby = self.get_baby(pk)
        serializer = BabySerializer(baby)

        return Response(serializer.data)

    def put(self, request, pk):
        serializer = BabySerializer(self.get_baby(pk))

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, pk):
        serializer = BabySerializer(self.get_baby(pk))

        return Response(serializer.data)
  