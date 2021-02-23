  
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import client
from django.test.client import Client
from .models import Profile, CustomUser, Baby
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import response, status
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.utils.user_authentication import authenticate_user

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# def create_fake_login_token(email, password):
#     def _method_wrapper(function):
#         def wrapper(*args, **kwargs):
#             # print(email)
#             # print(password)
#             client = Client()
#             url = reverse("login")
#             data = {"email": email, "password": password}
#             response_login = client.post(url, data, format="json")

#             print(response_login.data)

#             # access_token = response_login.json()["token"]["access"]
#             access_token = response_login.json()["access"]
#             # access_token = response_login.json()["token"]["token"]["access"]
#             kwargs["access_token"] = f"Bearer {access_token}"
#             return function(*args, **kwargs)

#         return wrapper

#     return _method_wrapper
"""""" """""" """""" """""" """""" """""" """""" """""" """"""
"""Funkcje tworzą instancje Profile z gotowym User """
"""""" """""" """""" """""" """""" """""" """""" """""" """"""


def user_factory(**kwargs):
    return User.objects.create_user(**kwargs)

def profile_factory(email=None, password=None, user=None, account_status=None):
    if not user:
        user = user_factory(email=email, password=password)
    profile = Profile.objects.create(user=user)
    if account_status:
        profile.save()
    return profile

def baby_factory(
    baby_name=None, 
    baby_birth=None, 
    baby_gender=None, 
    baby_weight=None, 
    baby_height=None, 
    profile_id=None
    ):
    baby = Baby.objects.create(
        baby_name = baby_name,
        baby_birth = baby_birth,
        baby_gender =baby_gender,
        baby_weight = baby_weight,
        baby_height = baby_height,
        profile_id = profile_id
        )
    baby.save()
    return baby
class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser("super@user.com", "foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )


class ProfileTests(TestCase):
    def setUp(self):
        self.test_user = 1
        self.test_name = "Wiesław"
        self.test_profile_birth = "2020-03-12"
        self.test_postal_code = "04-076"
        self.test_address = "Iżycka 21, Warszawa"
        self.test_gender = "Male"
        return super().setUp()

    def test_profile_creation(self):
        user = CustomUser.objects.create(id=1)
        profile = Profile.objects.create(
            user=user,
            name="Wiesław",
            profile_birth="2020-03-12",
            postal_code="04-076",
            address="Iżycka 21, Warszawa",
            gender="Male",
        )
        self.assertEqual(profile.id, 1)
        self.assertEqual(profile.name, self.test_name)
        self.assertEqual(profile.profile_birth, self.test_profile_birth)
        self.assertEqual(profile.postal_code, self.test_postal_code)
        self.assertEqual(profile.address, self.test_address)
        self.assertEqual(profile.gender, self.test_gender)


class BabyTests(TestCase):
    def setUp(self):
        self.test_user = 1
        self.test_profile = 1
        self.test_baby_name = "Wiesław"
        self.test_baby_birth = "2020-03-12"
        self.test_baby_gender = "Chłopiec"
        self.test_baby_weight = "4 Kg"
        self.test_baby_height = "57 cm"
        return super().setUp()

    def test_profile_creation(self):
        user = CustomUser.objects.create(id=1)
        profile = Profile.objects.create(user=user)
        baby = Baby.objects.create(
            profile=profile,
            baby_name="Wiesław",
            baby_birth="2020-03-12",
            baby_gender="Chłopiec",
            baby_weight="4 Kg",
            baby_height="57 cm",
        )
        self.assertEqual(baby.id, 1)
        self.assertEqual(baby.baby_name, self.test_baby_name)
        self.assertEqual(baby.baby_birth, self.test_baby_birth)
        self.assertEqual(baby.baby_gender, self.test_baby_gender)
        self.assertEqual(baby.baby_weight, self.test_baby_weight)
        self.assertEqual(baby.baby_height, self.test_baby_height)


class AccountTests(APITestCase):
    def test_create_account(self):
        user = get_user_model()
        url = reverse("register")
        data = {
            "email": "info@gmail.pl",
            "password": "qweqwe1!",
            "password2": "qweqwe1!",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.objects.count(), 1)
        self.assertEqual(user.objects.get().email, "info@gmail.pl")


    def test_login(self):
        user = get_user_model()
        user1 = user.objects.create_user(email="normal@user.com", password="foo")
        response = self.client.post(
            reverse("login"), {"email": "normal@user.com", "password": "foo"}
        )
        access_token = response.json()["access"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(access_token), str)


class ProfileListViewApiTests(APITestCase):
    def setUp(self):
        self.profile = profile_factory(email="normal@user.com", password="foo")
        self.client = APIClient()
        return super().setUp()

    def test_profile_patch(self):

        url = reverse("login")
        data = {"email": "normal@user.com", "password": "foo"}
        response_post = self.client.post(url, data, format="json")
        access_token = response_post.json()['access']

        url = reverse("profile")
        data = {
            "name": "Wiesław",
            "profile_birth": "2020-03-12",
            "postal_code": "04-076",
            "address": "Iżycka 21, Warszawa",
            "gender": "Male",
        }
        user_token = self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        response_patch = self.client.patch(
            url, data, format="json", HTTP_AUTHORIZATION=user_token
        )

        self.assertEqual(response_patch.data["name"], "Wiesław")

        response_get = self.client.get(
            url, data, format="json", HTTP_AUTHORIZATION=user_token
        )
        self.assertEqual(response_get.data["name"], "Wiesław")
class BabyTests(TestCase):
    def setUp(self):
        self.test_user = 1
        self.test_profile = 1
        self.test_baby_name = "Wiesław"
        self.test_baby_birth = "2020-03-12"
        self.test_baby_gender = "Chłopiec"
        self.test_baby_weight = "4 Kg"
        self.test_baby_height = "57 cm"
        return super().setUp()

    def test_profile_creation(self):
        user = CustomUser.objects.create(id=1)
        profile = Profile.objects.create(user=user)
        baby = Baby.objects.create(
            profile=profile,
            baby_name="Wiesław",
            baby_birth="2020-03-12",
            baby_gender="Chłopiec",
            baby_weight="4 Kg",
            baby_height="57 cm",
        )
        self.assertEqual(baby.id, 1)
        self.assertEqual(baby.baby_name, self.test_baby_name)
        self.assertEqual(baby.baby_birth, self.test_baby_birth)
        self.assertEqual(baby.baby_gender, self.test_baby_gender)
        self.assertEqual(baby.baby_weight, self.test_baby_weight)
        self.assertEqual(baby.baby_height, self.test_baby_height)


class AccountTests(APITestCase):
    def test_create_account(self):
        user = get_user_model()
        url = reverse("register")
        data = {
            "email": "info@gmail.pl",
            "password": "qweqwe1!",
            "password2": "qweqwe1!",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.objects.count(), 1)
        self.assertEqual(user.objects.get().email, "info@gmail.pl")
        return user

      
class BabyListTest(APITestCase):
    def setUp(self):
        self.profile = profile_factory(email="normal@user.com", password="foo")
        self.client = APIClient()
        return super().setUp()

    def get_token(self):
        url = reverse("login")
        data = {"email": "normal@user.com", "password": "foo"}
        response_post = self.client.post(url, data, format="json")
        access_token = response_post.json()['access']
        return access_token

    def test_baby_list_post(self):
        url = reverse('baby_list')
        data = {
            'baby_name': 'Adolf',
            'baby_birth': '1889-04-20',
            'baby_gender': 'Boy',
            'baby_weight': '4',
            'baby_height': '60'
        }
        user_token = self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.get_token()}"
        )

        response_post = self.client.post(
            url, data, format="json", HTTP_AUTHORIZATION=user_token
        )
        self.assertEqual(response_post.data['baby_name'], 'Adolf')

        response_get = self.client.get(
            url, format="json", HTTP_AUTHORIZATION=user_token
        )

        self.assertEqual(response_get.data[0]['baby_name'], 'Adolf')
        self.assertEqual(response_get.status_code, 200)

    def test_baby_list_get(self):
        url = reverse('baby_list')

        user_token = self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.get_token()}"
        )

        baby = baby_factory(
            baby_name='Adolf', 
            baby_birth='1889-04-20', 
            baby_gender = 'Boy',
            baby_weight = 60,
            baby_height = 60,
            profile_id = Profile.objects.get(id=1).id,
            )


        response_get = self.client.get(
            url, format="json", HTTP_AUTHORIZATION=user_token
        )

        self.assertEqual(response_get.data[0]['baby_name'], 'Adolf')
        self.assertEqual(response_get.status_code, 200)      


class BabyDetailsTest(APITestCase):
    def setUp(self):
        self.profile = profile_factory(email="normal@user.com", password="foo")

        profile_id = Profile.objects.get(id=1).id

        self.baby = baby_factory(
            baby_name='Adolf', 
            baby_birth='1889-04-20', 
            baby_gender = 'Boy',
            baby_weight = 60,
            baby_height = 60,
            profile_id = profile_id,
        )
        self.client = APIClient()
        return super().setUp()

    def get_token(self):
        url = reverse("login")
        data = {"email": "normal@user.com", "password": "foo"}
        response_post = self.client.post(url, data, format="json")
        access_token = response_post.json()['access']
        return access_token

    def fetch_baby_id(self):
        babies = Baby.objects.all()
        return babies[0].id

    def test_baby_details_get(self):
        baby_pk = self.fetch_baby_id()

        url = reverse('baby', args=[baby_pk])

        user_token = self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.get_token()}"
        )

        response_get = self.client.get(
            url, format="json", HTTP_AUTHORIZATION=user_token
        )
      

        self.assertEqual(response_get.data['baby_name'], 'Adolf')
        self.assertEqual(response_get.data['baby_birth'], '1889-04-20')
        self.assertEqual(response_get.data['baby_gender'], 'Boy')
        self.assertEqual(response_get.data['baby_weight'], '60')
        self.assertEqual(response_get.data['baby_height'], '60')
        self.assertEqual(response_get.status_code, 200)      

    def test_baby_details_patch(self):
        baby_pk = self.fetch_baby_id()
        url = reverse('baby', args=[baby_pk])

        user_token = self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.get_token()}"
        )

        data = {
            "baby_name": 'Karol',
            "baby_birth": '1889-04-20',
        }

        response_patch = self.client.patch(
            url, data, format="json", HTTP_AUTHORIZATION=user_token
        )

        self.assertEqual(response_patch.data['baby_name'], 'Karol')
        self.assertEqual(response_patch.data['baby_birth'], '1889-04-20')
        self.assertEqual(response_patch.data['baby_gender'], 'Boy')
        self.assertEqual(response_patch.data['baby_weight'], '60')
        self.assertEqual(response_patch.data['baby_height'], '60')
        self.assertEqual(response_patch.status_code, 200)   

# class CategoryListViewApiTests(APITestCase):
#     def setUp(self):
#         self.profile = profile_factory(
#             email="example_1@user.com", password="bar", account_status=AccountStatus.NPU
#         )
#         self.profile2 = profile_factory(
#             email="example_2@user.com", password="bar", account_status=AccountStatus.NPU
#         )
#         self.category_data_set = {
#             "profile": "1",
#             "name": "Samochód",
#             "short_name": "AUT",
#             "description": "Wydatki na samochód",
#         }
#         return super().setUp()

#     @create_fake_login_token("example_1@user.com", "bar")
#     def test_category_post(self, **kwargs):
#         url = reverse("categories")
#         response_category_post = self.client.post(
#             url,
#             self.category_data_set,
#             format="json",
#             HTTP_AUTHORIZATION=kwargs["access_token"],
#         )
#         response_category_post_no_token = self.client.post(
#             url,
#             self.category_data_set,
#             format="json",
#         )
#         self.assertEqual(response_category_post.data["name"], "Samochód")
#         self.assertEqual(response_category_post.status_code, 201)
#         self.assertEqual(response_category_post_no_token.status_code, 401)

