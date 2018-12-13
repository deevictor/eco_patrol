from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from mezzanine.accounts.admin import UserProfileAdmin

from .models import City, User


class UserAdmin(UserProfileAdmin):
    """Админка пользователя."""

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'last_name', 'first_name', 'middle_name',
                'email', 'phone', 'city',
                'registration', 'education'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_inspector', 'is_active', 'is_staff',
                'is_superuser', 'groups', 'user_permissions'
            )
        }),
        (_('Important dates'), {
            'fields': (
                'last_login', 'date_joined'
            )
        }),
    )

    list_display = (
        'username', 'first_name', 'last_name',
        'is_inspector', 'is_active', 'is_staff',
        'is_superuser', 'last_login', 'date_joined'
    )
    list_editable = ('is_inspector',)
    list_filter = (
        'is_inspector', 'is_staff', 'is_active',
        'is_superuser'
    )


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'type_of_region',)
    list_filter = ('region', 'type_of_region',)
    search_fields = ('name',)


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(User, UserAdmin)
admin.site.register(City, CityAdmin)
