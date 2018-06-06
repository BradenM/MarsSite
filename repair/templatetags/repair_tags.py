from django import template
from ..forms import SelectDeviceForm

register = template.Library()

@register.inclusion_tag('repair/family_modal.html')
def family_modal(family):
    devs = family.devices.all()
    form = SelectDeviceForm()
    form.fields['devices'].queryset = devs
    return {'form': form, 'fam': family}