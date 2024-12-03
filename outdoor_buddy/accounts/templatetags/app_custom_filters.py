from django import template

from outdoor_buddy.accounts.models import Contact

register = template.Library()


@register.filter
def contact(user):
    try:
        return Contact.objects.get(user=user)
    except Contact.DoesNotExist:
        return None



