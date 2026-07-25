from django.contrib import admin
# pyrefly: ignore [missing-import]
from .models import Blog,Profile
# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=("title","author","status","created_at")

    search_fields=("title","content")
    list_filter=("status","created_at")
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=("user","bio","profile_image")
    search_fields=("user","bio")
    list_filter=["user"]
    