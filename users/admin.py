from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ['username', 'is_superuser', 'is_workstudy', 'default_password_used']
    fieldsets = UserAdmin.fieldsets + (
        (_('User Type'), {'fields': ('is_workstudy', 'default_password_used')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('User Type'), {'fields': ('is_workstudy',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)