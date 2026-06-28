from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm



@admin.register(User)
class UserAdmin(BaseUserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
     ) 


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    add_form = ProfileForm
    form = ProfileForm

    list_display = ('user', 'role', 'bio', 'avatar')
    list_filter = ('role',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'bio') 

