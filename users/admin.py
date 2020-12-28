from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Profile, Baby


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['user']
    list_filter = ('name',)
    search_fields = ('gender',)


@admin.register(Baby)
class BabyAdmin(admin.ModelAdmin):
    exclude = [""]               # wszystkie pola oprócz: ""
    list_display = ["baby_name",]   # pola do wyśiwetlenia na liście
    list_filter = ('baby_gender',)          # filtrowanie po rpawej stronie
    search_fields = ('baby_name',)          # wyszukiwanie po polu


