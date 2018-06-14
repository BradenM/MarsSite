from django import template
from djstripe.models import Customer
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

@register.simple_tag(name="default_card")
def get_default_card(customer, source):
    card = customer.sources.get(pk=source)
    #default = customer.api_retrieve(settings.STRIPE_TEST_SECRET_KEY, {'default_source'})
    #print(default)
    # print(card.id)
    print(customer.default_source)
    return ''