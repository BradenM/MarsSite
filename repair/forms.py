from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, ButtonHolder, Div, Fieldset, Layout, HTML
from .models import Family
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect



class SelectDeviceForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ("devices",)
        widgets = {
            'devices': forms.Select(attrs={'class':'select is-rounded'})
        }

    def __init__(self, *args, **kwargs):
        super(SelectDeviceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        # self.helper.layout = Layout(
        #     HTML("""
        #         <div class='select'>
        #             <select id='selected_device' class='select is-rounded' name='selected_device'>
        #                 {{ devices }}
        #             </select>
        #         </div>
        #         <input type='submit' value='Repair' class='button is-info'/>
        #     """),
        # )

        self.helper.layout = Layout(
            Div(
                Div(
                'Legend of fieldsets',
                'devices',
                css_class="select"
                ),
            ),
            Div(
                Div(
                    Submit('submit', 'Repair', css_class="button is-info"), 
                )
            ),
        )
        #self.helper.add_input(Submit('submit', 'Repair', css_class="button is-info"))