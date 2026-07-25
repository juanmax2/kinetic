from django.contrib import admin
from .models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'weight', 'height', 'goal', 'daily_calories_target')
    search_fields = ('user__username',)