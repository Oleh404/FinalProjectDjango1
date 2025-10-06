from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from fin_project.apps.users.models import User

class CustomUserAdmin(BaseUserAdmin):
    actions = ['make_landlord']

    def make_landlord(self, queryset):
        queryset.update(user_type='landlord')
    make_landlord.short_description = "Make landlord"

    def get_user_type_display(self, obj):
        return obj.get_user_type_display()
    get_user_type_display.short_description = "User Type"

    list_display = ('email',  'get_user_type_display', 'is_staff')
    list_filter = ('user_type', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone_number',),}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser')}),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2', 'user_type'),
        }),
    )

    search_fields = ('email', )
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)


