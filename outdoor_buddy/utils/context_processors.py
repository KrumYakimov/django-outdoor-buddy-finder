from outdoor_buddy.accounts.models import Profile


def add_profile_to_context(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            return {"profile": profile}
        except Profile.DoesNotExist:
            return {"profile": None}
    return {"profile": None}
