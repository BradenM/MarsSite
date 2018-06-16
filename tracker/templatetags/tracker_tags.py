from django import template
from django.conf import settings
from tracker.models import STATUS_CHOICES

register = template.Library()


@register.inclusion_tag('tracker/step.html', name="get_status")
def get_step_status(tracker):

    status = [i[0] for i in STATUS_CHOICES]
    updates = tracker.updates.all()

    latest = tracker.updates.last()
    complete = []
    incomplete = []

    for i, choice in enumerate(status):
        try:
            complete.append(updates[i])
        except IndexError:
            incomplete.append(choice)

    return {'complete': complete, 'incomplete': incomplete, 'latest': latest}
