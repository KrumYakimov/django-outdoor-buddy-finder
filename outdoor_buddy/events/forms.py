from django import forms
from outdoor_buddy.events.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["id", "creator"]
        widgets = {
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "registration_deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "description": forms.Textarea(attrs={"rows": 4}),
            "picture_upload": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "id": "picture-upload-input",
                }
            ),
        }
