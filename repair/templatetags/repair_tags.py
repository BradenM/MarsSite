from django import template
from ..forms import SelectDeviceForm

register = template.Library()

@register.inclusion_tag('repair/family_modal.html')
def family_modal(family):
    devs = family.devices.all()
    form = SelectDeviceForm()
    form.fields['devices'].queryset = devs
    return {'form': form, 'fam': family}

# A hackish way of getting base device url
@register.filter(name="url_base")
def url_base(value):
    split = value.split('/')
    del split[-2:]
    redirect = "/".join([x for x in split])
    return redirect
