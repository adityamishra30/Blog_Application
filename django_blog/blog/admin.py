from django.contrib import admin
# pyrefly: ignore [missing-import]
from .models import Blog
# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=("title","author","status","created_at")

    search_fields=("title","content")
    list_filter=("status","created_at")