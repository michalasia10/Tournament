from django.contrib import admin

from tournament.models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = True
    verbose_name = 'user profile'
    verbose_name_plural = 'user profiles'
