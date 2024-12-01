from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from outdoor_buddy.accounts.models import Profile, Contact

UserModel = get_user_model()


# class CustomAuthenticationForm(auth_forms.AuthenticationForm):
#     username = forms.CharField(label="Email")
#     password = forms.CharField(label="Password")


class AppUserCreationForm(auth_forms.UserCreationForm):
    # email = forms.EmailField(label="Email")
    # password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    # password2 = forms.CharField(widget=forms.PasswordInput, label="Repeat Password")

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ("email",)


# class CustomPasswordChangeForm(PasswordChangeForm):
#     old_password = forms.CharField(
#         label="Current Password",
#         widget=forms.PasswordInput(attrs={"placeholder": "Enter your current password"})
#     )
#     new_password1 = forms.CharField(
#         label="New Password",
#         widget=forms.PasswordInput(attrs={"placeholder": "Enter a new password"})
#     )
#     new_password2 = forms.CharField(
#         label="Confirm New Password",
#         widget=forms.PasswordInput(attrs={"placeholder": "Confirm your new password"})
#     )

class AccountEmailChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already taken.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'date-of-birth',
            }),
            'picture_upload': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'picture-upload-input',
            }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ["user"]


