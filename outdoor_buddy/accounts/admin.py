from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.contrib.admin import SimpleListFilter
from unfold.admin import ModelAdmin, StackedInline, TabularInline
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
class AppUserAdmin(ModelAdmin):
    inlines = [ProfileInline, ContactFormInline]
    list_display = (
        "email",
        "date_joined",
        "is_active",
        "is_staff",
        "has_profile",
        "has_contact",
    )
    list_filter = ("is_active", "is_staff", UsersWithProfileFilter)
    search_fields = ("email",)
    ordering = ("-date_joined", "email")
    readonly_fields = ("date_joined",)
    fieldsets = (
        ("Basic Info", {"fields": ("email", "date_joined", "is_active")}),
        ("Permissions", {
            "fields": ("is_staff", "is_superuser", "groups"),
            "classes": ["collapse"],  # Makes this section collapsible
        }),
    )

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)

    mark_as_active.short_description = "Mark selected users as active"

    actions = [mark_as_active]

    @admin.display(boolean=True, description="Has Profile")
    def has_profile(self, obj):
        return hasattr(obj, "profile")

    @admin.display(boolean=True, description="Has Contact")
    def has_contact(self, obj):
        return hasattr(obj, "contact")


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
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
