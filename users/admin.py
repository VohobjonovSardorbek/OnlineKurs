from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Account, Student


@admin.register(Account)
class CustomAccountAdmin(UserAdmin):
    model = Account

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


admin.site.register(Student)
