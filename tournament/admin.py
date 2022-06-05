from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from tournament.models import UserProfile, Stage, Tournament, Team, Match


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = True
    verbose_name = 'user profile'
    verbose_name_plural = 'user profiles'


class CustomUserAdmin(UserAdmin):
    list_display = ('id',) + UserAdmin.list_display
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Stage)
admin.site.register(Team)
admin.site.register(Tournament)
admin.site.register(Match)
