from django.contrib import admin
from .models import User, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 1

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'date_joined', 'role')
    search_fields = ('email', 'role')
    inlines = [UserProfileInline]


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['email']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active')}),
    )

admin.site.register(UserProfile)
admin.site.register(User, CustomUserAdmin)