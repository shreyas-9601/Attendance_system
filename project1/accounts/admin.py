from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    search_fields = ('username', 'division')
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'division', 'image', 'is_staff', ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('division', 'image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('division', 'image')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)