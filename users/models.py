from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    date_last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class MyModel(models.Model):
    class ProfileGender(models.TextChoices):
        MAL = 'Male', "Mężczyzna"
        FEM = 'Female', "Kobieta"
        UNN = 'Unknown', "Nie Wybrano"

    class BabyGender(models.TextChoices):
        BOY = 'Boy', "Chłopiec"
        GRL = "Girl", "Dziewczynka"
        UNN = 'Unknown', "Nie Wybrano"

    class Weight(models.TextChoices):
        UNN = 0, "Nie Wybrano"
        kg1 = 1, '1 kg'
        kg2 = 2, '2 kg'
        kg3 = 3, '3 kg'
        kg4 = 4, '4 kg'
        kg5 = 5, '5 kg'
        kg6 = 6, '6 kg'
        kg7 = 7, '7 kg'
        kg8 = 8, '8 kg'
        kg9 = 9, '9 kg'
        kg10 = 10, '10 kg'
        kg11 = 11, '11 kg'
        kg12 = 12, '12 kg'
        kg13 = 13, '13 kg'
        kg14 = 14, '14 kg'
        kg15 = 15, '15 kg'
        kg16 = 16, '16 kg'
        kg17 = 17, '17 kg'
        kg18 = 18, '18 kg'
        kg19 = 19, '19 kg'
        kg20 = 20, '20 kg'
        kg21 = 21, '21 kg'
        kg22 = 22, '22 kg'
        kg23 = 23, '23 kg'
        kg24 = 24, '24 kg'
        kg25 = 25, '25 kg'
        kg26 = 26, '26 kg'
        kg27 = 27, '27 kg'
        kg28 = 28, '28 kg'
        kg29 = 29, '29 kg'
        kg30 = 30, '30 kg'
        kg31 = 31, '31 kg'
        kg32 = 32, '32 kg'
        kg33 = 33, '33 kg'
        kg34 = 34, '34 kg'
        kg35 = 35, '35 kg'
        kg36 = 36, '36 kg'
        kg37 = 37, '37 kg'
        kg38 = 38, '38 kg'
        kg39 = 39, '39 kg'
        kg40 = 40, '40 kg'
        kg41 = 41, '41 kg'
        kg42 = 42, '42 kg'
        kg43 = 43, '43 kg'
        kg44 = 44, '44 kg'
        kg45 = 45, '45 kg'
        kg46 = 46, '46 kg'
        kg47 = 47, '47 kg'
        kg48 = 48, '48 kg'
        kg49 = 49, '49 kg'
        kg50 = 50, '50 kg'
        kg51 = 51, '51 kg'
        kg52 = 52, '52 kg'
        kg53 = 53, '53 kg'
        kg54 = 54, '54 kg'
        kg55 = 55, '55 kg'
        kg56 = 56, '56 kg'
        kg57 = 57, '57 kg'
        kg58 = 58, '58 kg'
        kg59 = 59, '59 kg'
        kg60 = 60, '60 kg'
        kg61 = 61, '61 kg'
        kg62 = 62, '62 kg'
        kg63 = 63, '63 kg'
        kg64 = 64, '64 kg'
        kg65 = 65, '65 kg'
        kg66 = 66, '66 kg'
        kg67 = 67, '67 kg'
        kg68 = 68, '68 kg'
        kg69 = 69, '69 kg'
        kg70 = 70, '70 kg'
        kg71 = 71, '71 kg'
        kg72 = 72, '72 kg'
        kg73 = 73, '73 kg'
        kg74 = 74, '74 kg'
        kg75 = 75, '75 kg'
        kg76 = 76, '76 kg'
        kg77 = 77, '77 kg'
        kg78 = 78, '78 kg'
        kg79 = 79, '79 kg'
        kg80 = 80, '80 kg'
        kg81 = 81, '81 kg'
        kg82 = 82, '82 kg'
        kg83 = 83, '83 kg'
        kg84 = 84, '84 kg'
        kg85 = 85, '85 kg'
        kg86 = 86, '86 kg'
        kg87 = 87, '87 kg'
        kg88 = 88, '88 kg'
        kg89 = 89, '89 kg'
        kg90 = 90, '90 kg'
        kg91 = 91, '91 kg'
        kg92 = 92, '92 kg'
        kg93 = 93, '93 kg'
        kg94 = 94, '94 kg'
        kg95 = 95, '95 kg'
        kg96 = 96, '96 kg'
        kg97 = 97, '97 kg'
        kg98 = 98, '98 kg'
        kg99 = 99, '99 kg'

    class Height(models.TextChoices):
        UNN = 0, "Nie Wybrano"
        cm25 = 25, "25cm"
        cm26 = 26, "26cm"
        cm27 = 27, "27cm"
        cm28 = 28, "28cm"
        cm29 = 29, "29cm"
        cm30 = 30, "30cm"
        cm31 = 31, "31cm"
        cm32 = 32, "32cm"
        cm33 = 33, "33cm"
        cm34 = 34, "34cm"
        cm35 = 35, "35cm"
        cm36 = 36, "36cm"
        cm37 = 37, "37cm"
        cm38 = 38, "38cm"
        cm39 = 39, "39cm"
        cm40 = 40, "40cm"
        cm41 = 41, "41cm"
        cm42 = 42, "42cm"
        cm43 = 43, "43cm"
        cm44 = 44, "44cm"
        cm45 = 45, "45cm"
        cm46 = 46, "46cm"
        cm47 = 47, "47cm"
        cm48 = 48, "48cm"
        cm49 = 49, "49cm"
        cm50 = 50, "50cm"
        cm51 = 51, "51cm"
        cm52 = 52, "52cm"
        cm53 = 53, "53cm"
        cm54 = 54, "54cm"
        cm55 = 55, "55cm"
        cm56 = 56, "56cm"
        cm57 = 57, "57cm"
        cm58 = 58, "58cm"
        cm59 = 59, "59cm"
        cm60 = 60, "60cm"
        cm61 = 61, "61cm"
        cm62 = 62, "62cm"
        cm63 = 63, "63cm"
        cm64 = 64, "64cm"
        cm65 = 65, "65cm"
        cm66 = 66, "66cm"
        cm67 = 67, "67cm"
        cm68 = 68, "68cm"
        cm69 = 69, "69cm"
        cm70 = 70, "70cm"
        cm71 = 71, "71cm"
        cm72 = 72, "72cm"
        cm73 = 73, "73cm"
        cm74 = 74, "74cm"
        cm75 = 75, "75cm"
        cm76 = 76, "76cm"
        cm77 = 77, "77cm"
        cm78 = 78, "78cm"
        cm79 = 79, "79cm"
        cm80 = 80, "80cm"
        cm81 = 81, "81cm"
        cm82 = 82, "82cm"
        cm83 = 83, "83cm"
        cm84 = 84, "84cm"
        cm85 = 85, "85cm"
        cm86 = 86, "86cm"
        cm87 = 87, "87cm"
        cm88 = 88, "88cm"
        cm89 = 89, "89cm"
        cm90 = 90, "90cm"
        cm91 = 91, "91cm"
        cm92 = 92, "92cm"
        cm93 = 93, "93cm"
        cm94 = 94, "94cm"
        cm95 = 95, "95cm"
        cm96 = 96, "96cm"
        cm97 = 97, "97cm"
        cm98 = 98, "98cm"
        cm99 = 99, "99cm"
        cm100 = 100, "100cm"
        cm101 = 101, "101cm"
        cm102 = 102, "102cm"
        cm103 = 103, "103cm"
        cm104 = 104, "104cm"
        cm105 = 105, "105cm"
        cm106 = 106, "106cm"
        cm107 = 107, "107cm"
        cm108 = 108, "108cm"
        cm109 = 109, "109cm"
        cm110 = 110, "110cm"
        cm111 = 111, "111cm"
        cm112 = 112, "112cm"
        cm113 = 113, "113cm"
        cm114 = 114, "114cm"
        cm115 = 115, "115cm"
        cm116 = 116, "116cm"
        cm117 = 117, "117cm"
        cm118 = 118, "118cm"
        cm119 = 119, "119cm"
        cm120 = 120, "120cm"
        cm121 = 121, "121cm"
        cm122 = 122, "122cm"
        cm123 = 123, "123cm"
        cm124 = 124, "124cm"
        cm125 = 125, "125cm"
        cm126 = 126, "126cm"
        cm127 = 127, "127cm"
        cm128 = 128, "128cm"
        cm129 = 129, "129cm"
        cm130 = 130, "130cm"
        cm131 = 131, "131cm"
        cm132 = 132, "132cm"
        cm133 = 133, "133cm"
        cm134 = 134, "134cm"
        cm135 = 135, "135cm"
        cm136 = 136, "136cm"
        cm137 = 137, "137cm"
        cm138 = 138, "138cm"
        cm139 = 139, "139cm"
        cm140 = 140, "140cm"
        cm141 = 141, "141cm"
        cm142 = 142, "142cm"
        cm143 = 143, "143cm"
        cm144 = 144, "144cm"
        cm145 = 145, "145cm"
        cm146 = 146, "146cm"
        cm147 = 147, "147cm"
        cm148 = 148, "148cm"
        cm149 = 149, "149cm"
        cm150 = 150, "150cm"

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=True, null=True)
    profile_birth = models.DateField(blank=True, null=True)
    postal_code = models.CharField(max_length=6, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    gender = models.CharField(max_length=11, choices=MyModel.ProfileGender.choices, default=MyModel.ProfileGender.UNN)

    def __str__(self):
        return self.name


class Baby(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    baby_name = models.CharField(max_length=64, blank=True, null=True)
    baby_birth = models.DateField()
    baby_gender = models.CharField(max_length=11, choices=MyModel.BabyGender.choices, default=MyModel.BabyGender.UNN)
    baby_weight = models.CharField(max_length=7, choices=MyModel.Weight.choices, default=MyModel.Weight.UNN)
    baby_height = models.CharField(max_length=7, choices=MyModel.Height.choices, default=MyModel.Height.UNN)

    def __str__(self):
        return self.baby_name
