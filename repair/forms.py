from django import forms
from .models import Device

class SortForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['brand']
        widgets = {
            'brand': forms.Select(attrs={'onchange': 'this.form.submit();'})
        }
