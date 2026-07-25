from django import forms 
# pyrefly: ignore [missing-import]
from . models import Blog,Profile

class BlogForm(forms.ModelForm):
    class Meta:
        model =Blog
        fields=["title",
        "content",
        "cover_image",
        "status",
        "is_ai_generated",
        "generation_topic"]
        widgets = {
            "is_ai_generated": forms.HiddenInput(),
            "generation_topic": forms.HiddenInput(),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=["profile_image","bio"]
        
