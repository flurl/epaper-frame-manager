from django import forms
from .models import Firmware

class FirmwareUpload(forms.ModelForm):
    class Meta:
        model = Firmware
        fields = ['file']