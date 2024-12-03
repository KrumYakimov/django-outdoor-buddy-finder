from django import template

from outdoor_buddy.accounts.models import Contact

register = template.Library()


@register.filter
def placeholder(value, token):
    """Set a placeholder attribute on the field's widget."""
    value.field.widget.attrs["placeholder"] = token
    return value



