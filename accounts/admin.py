from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile
from .forms import UserAdminCreationForm, UserAdminForm


class ProfileInline(admin.StackedInline):
     model = Profile
     max_num = 1
     can_delete = False


class UserAdmin(BaseUserAdmin):

    add_form = UserAdminCreationForm
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )
    form = UserAdminForm
    fieldsets = (
        (None, {
            'fields': ('username', 'email')
        }),
        ('Informações Básicas', {
            'fields': ('username', 'last_login')
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
    list_display = ['username', 'email', 'is_active', 'is_staff', 'date_joined']
    inlines = [ProfileInline]


admin.site.register(User, UserAdmin)
