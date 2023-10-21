from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = 'user', 'id', 'fullName', 'email', 'phone', 'avatar'


admin.site.register(Profile, ProfileAdmin)
