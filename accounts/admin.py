from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm, UserAdminForm

class UserAdmin(BaseUserAdmin):
    form = UserCreationForm
    add_fieldsets = (
            (None, {
                'fields': ('email', 'password1', 'password2')
                }),
            )
    form = UserAdminForm
    fieldsets = (
        (None, {
            'fields': ('email')
        }),
        ('Informações Básicas', {
            'fields': ('email', 'last_login')
        }),
        (
            'Permissões', {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser', 'groups',
                    'user_permissions'
                )
            }
        ),
    )
    list_display = ['email', 'is_staff', 'is_active',
                    'date_joined']


admin.site.register(User, UserAdmin)
