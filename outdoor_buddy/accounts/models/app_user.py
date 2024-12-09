from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _

from outdoor_buddy.accounts.managers import AppUserManager


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    """
    Custom user model for the Outdoor Buddy application.
    Extends Django's AbstractBaseUser and PermissionsMixin to provide a flexible user model
    with email as the unique identifier instead of a username.
    """
    EMAIL_VALIDATION_ERROR_MASSAGE = "This email is already used by another user"

    class Meta:
        verbose_name = "Application User"
        verbose_name_plural = "Application Users"
        ordering = ["email"]

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"

    objects = AppUserManager()
