from django import forms 
# pyrefly: ignore [missing-import]
from . models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model =Blog
        fields=["title",
        "content",
        "cover_image",
        "status"]
