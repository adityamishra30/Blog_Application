from django import forms 
# pyrefly: ignore [missing-import]
from . models import Blog,Profile

class BlogForm(forms.ModelForm):
    class Meta:
        model =Blog
        fields=["title",
        "content",
        "cover_image",
        "status"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=["profile_image","bio"]
        
