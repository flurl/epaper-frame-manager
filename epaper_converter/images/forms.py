from django import forms
from django.forms import ClearableFileInput
from .models import Image

class ImageUpload(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['original_image']