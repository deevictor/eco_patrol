from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from mezzanine.accounts.admin import UserProfileAdmin

from .models import User


class UserAdmin(UserProfileAdmin):
    """Админка пользователя."""

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'middle_name', 'email', 'phone',
                'city'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'
            )
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
