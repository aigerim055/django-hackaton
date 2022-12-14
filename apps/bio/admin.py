from django.contrib import admin

from .models import UserProfile, ProfileImage


class TabularInlineImages(admin.TabularInline):
    model = ProfileImage
    extra = 3
    fields = ['avatar']



class ProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    inlines = [TabularInlineImages]
    # exclude = ['cashback']

admin.site.register(UserProfile, ProfileAdmin)
