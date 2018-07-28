from .models import UserPayment, PaymentCard
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from pinax.stripe.actions import sources, customers
import stripe

# Delete Stripe Card along with PaymentCard instance


@receiver(pre_delete, sender=UserPayment)
def delete_stripe_card(sender, instance, **kwargs):
    if instance.type == 'card':
        customer = customers.get_customer_for_user(instance.user)
        try:
            sources.delete_card(customer, instance.stripe_id)
        except stripe.error.InvalidRequestError:
            pass
