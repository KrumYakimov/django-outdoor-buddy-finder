from django.contrib.auth import get_user_model
from django.shortcuts import render

UserModel = get_user_model()


class ReadOnlyFormMixin:
    """
    A mixin to make all fields in a form read-only.
    """

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Make all fields read-only or disabled
        for field_name, field in form.fields.items():
            if field.widget.__class__.__name__ == "Select":  # For dropdown fields
                field.widget.attrs['disabled'] = True
            else:
                field.widget.attrs['readonly'] = True
        return form


class UserIsOwnerMixin:
    """
    A mixin to restrict access to object owners only.
    """

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()

        if isinstance(object, UserModel):
            if object != request.user:
                return render(request, "response_status_codes/403.html", status=403)
        elif hasattr(object, "user"):
            if object.user != request.user:
                return render(request, "response_status_codes/403.html", status=403)

        return super().dispatch(request, *args, **kwargs)
