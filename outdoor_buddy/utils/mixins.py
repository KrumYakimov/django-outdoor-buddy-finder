class ReadOnlyFormMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Make all fields read-only
        for field_name, field in form.fields.items():
            field.widget.attrs['readonly'] = True
        return form
