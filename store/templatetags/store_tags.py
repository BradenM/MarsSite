from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(name="cart_total")
def get_cart_total(cart):
    products = cart.products.all()
    total = 0
    for item in products:
        total += item.order.price
    total = '${:,.2f}'.format(total)
    return total


@register.simple_tag(name="get_card_image")
def get_card_image(source):

    CARD_BRANDS = {
        'visa': 'visa.png',
        'mastercard': 'mastercard.png',
        'discover': 'discover.png',
        'american express': 'express.png',
    }
    brand = source.brand.lower()
    if brand in CARD_BRANDS.keys():
        return f'/media/cards/{CARD_BRANDS[brand]}'

    return 'blank'


@register.simple_tag(name="default_source")
def get_default_source(source):
    default_id = source.customer.stripe_customer.default_source
    source_id = source.stripe_id
    if source_id == default_id:
        return "checked=checked"
    return ''


@register.simple_tag(name="format_phone")
def format_phone_number(number):
    try:
        result = "%s%s %s%s%s-%s%s%s-%s%s%s%s" % tuple(str(number))
    except TypeError:
        result = number
    return result
