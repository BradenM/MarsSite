from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# class SortForm(forms.ModelForm):
#     class Meta:
#         model = Device
#         fields = ['brand']
#         widgets = {
#             'brand': forms.Select(attrs={'onchange': 'this.form.submit();'})
#         }

class SelectDevice(forms.Form):
    devices = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        devices = kwargs.pop('devices')
        super(SelectDevice, self).__init__(*args, **kwargs)
        self.fields['devices'].choices = devices
        self.helper = FormHelper()
        self.helper.form_action = devices.slug
        self.helper.add_input(Submit('submit', 'Select', css_class="button is-primary"))
