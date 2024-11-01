from django.contrib import admin
from .models import User, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 1

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'date_joined', 'role')
    search_fields = ('email', 'role')
    inlines = [UserProfileInline]

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
