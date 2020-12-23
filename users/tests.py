from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile, CustomUser


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
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
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
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
                email='super@user.com', password='foo', is_superuser=False)


class ProfileTests(TestCase):

    def setUp(self):
        self.test_user = 1
        self.test_name = 'Wiesław'
        self.test_profile_birth = '2020-03-12'
        self.test_postal_code = '04-076'
        self.test_address = 'Iżycka 21, Warszawa'
        self.test_gender = 'Male'
        return super().setUp()

    def test_profile_creation(self):
        user = CustomUser.objects.create(id=1)
        profile = Profile.objects.create(user=user,
                                         name='Wiesław',
                                         profile_birth = '2020-03-12',
                                         postal_code='04-076',
                                         address = 'Iżycka 21, Warszawa',
                                         gender='Male'
                                         )
        self.assertEqual(profile.id, 1)
        self.assertEqual(profile.name, self.test_name)
        self.assertEqual(profile.profile_birth, self.test_profile_birth)
        self.assertEqual(profile.postal_code, self.test_postal_code)
        self.assertEqual(profile.address, self.test_address)
        self.assertEqual(profile.gender, self.test_gender)
