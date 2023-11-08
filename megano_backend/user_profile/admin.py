from django.contrib import admin

from .models import Profile, Avatar


class ProfileAdmin(admin.ModelAdmin):
    list_display = 'user', 'id', 'fullName', 'email', 'phone', 'avatar'


admin.site.register(Profile, ProfileAdmin)


class AvatarAdmin(admin.ModelAdmin):
    list_display = 'src', 'alt'


admin.site.register(Avatar, AvatarAdmin)
