from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.	from .forms import CustomUserCreationForm, CustomUserChangeForm
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Profile


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

