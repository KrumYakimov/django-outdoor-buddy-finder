from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from outdoor_buddy.accounts.forms import ProfileForm
from outdoor_buddy.accounts.models import Profile, Contact

UserModel = get_user_model()


class ProfileInline(StackedInline):
    model = Profile
    classes = ["collapse"]
    extra = 0  # No extra empty forms by default


class ContactFormInline(TabularInline):
    model = Contact
    classes = ["collapse"]
    extra = 0

    @admin.display(boolean=True, description="Is Completed")
    def is_completed(self, obj):
        return obj.is_completed


# Custom Filter: Users with and without a profile
class UsersWithProfileFilter(SimpleListFilter):
    title = "Has Profile"
    parameter_name = "has_profile"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(profile__isnull=False)
        elif self.value() == "no":
            return queryset.filter(profile__isnull=True)
        return queryset


@admin.register(UserModel)
class AppUserAdmin(ModelAdmin, UserAdmin):
    inlines = [ProfileInline, ContactFormInline]
    list_display = (
        "email",
        "date_joined",
        "is_active",
        "is_superuser",
        "is_staff",
        "get_user_groups",
    )
    list_filter = ("is_active", "is_superuser", "is_staff", UsersWithProfileFilter)
    search_fields = ("email",)
    ordering = ("-date_joined", "email")
    readonly_fields = ("date_joined",)
    fieldsets = (
        ("Basic Info", {"fields": ("email", "date_joined", "is_active")}),
        (
            "Permissions",
            {
                "fields": ("is_staff", "is_superuser", "groups"),
                "classes": ["collapse"],  # Makes this section collapsible
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        """
        Restrict System Administrators from creating or editing superusers and staff.
        """
        if not request.user.is_superuser:
            if obj.is_superuser or obj.is_staff:
                raise PermissionDenied(
                    "You do not have permission to create or edit superusers and staff."
                )
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        Restrict System Administrators from deleting superusers.
        """
        if not request.user.is_superuser and obj.is_superuser and obj.is_staff:
            raise PermissionDenied("You do not have permission to delete superusers.")
        super().delete_model(request, obj)

    def get_queryset(self, request):
        """
        Restrict System Administrators from viewing superusers in the admin list view.
        """
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)  # Exclude superusers
        return qs

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)

    mark_as_active.short_description = "Mark selected users as active"

    actions = [mark_as_active]

    @admin.display(description="Groups")
    def get_user_groups(self, obj):
        """
        Dynamically displays the user's group memberships.
        """
        return ", ".join(group.name for group in obj.groups.all()) or "No Groups"


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    form = ProfileForm

    list_display = (
        "user_email",
        "full_name",
        "gender",
        "age",
        "skill_level",
        "fitness_level",
    )
    list_display_links = ("user_email", "full_name")
    list_filter = ("gender", "skill_level", "fitness_level")
    search_fields = ("user__email", "first_name", "last_name")
    ordering = ("user__email",)

    fieldsets = (
        (
            "User Profile",
            {
                "fields": (
                    "picture_upload",
                    "first_name",
                    "last_name",
                    "date_of_birth",
                    "gender",
                ),
            },
        ),
        (
            "Preferences",
            {
                "fields": (
                    "preferred_activities",
                    "preferred_location",
                ),
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "skill_level",
                    "fitness_level",
                    "availability",
                    "bio",
                ),
            },
        ),
    )

    def user_email(self, obj):
        return obj.user.email

    user_email.admin_order_field = "user__email"
    user_email.short_description = "User Email"

    def full_name(self, obj):
        return obj.full_name or "N/A"

    full_name.short_description = "Full Name"


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ("user_email", "city", "address", "phone_number", "is_completed")
    list_filter = ("city",)
    search_fields = ("user__email", "city", "address", "phone_number")
    ordering = ("user__email",)

    def user_email(self, obj):
        return obj.user.email

    user_email.admin_order_field = "user__email"
    user_email.short_description = "User Email"

    @admin.display(boolean=True, description="Is Completed")
    def is_completed(self, obj):
        return obj.is_completed
