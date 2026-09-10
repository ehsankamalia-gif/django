from django.contrib.auth.models import Permission

# Framework/internal permissions that aren't meaningful "features" for
# an admin to hand out to staff members.
EXCLUDED_APP_LABELS = {'admin', 'contenttypes', 'sessions'}
EXCLUDED_CODENAMES = {
    'add_group', 'change_group', 'delete_group', 'view_group',
    'add_permission', 'change_permission', 'delete_permission', 'view_permission',
}


def assignable_permissions():
    """Permissions an Admin is allowed to grant to a staff member."""
    return (
        Permission.objects
        .select_related('content_type')
        .exclude(content_type__app_label__in=EXCLUDED_APP_LABELS)
        .exclude(codename__in=EXCLUDED_CODENAMES)
        .order_by('content_type__app_label', 'content_type__model', 'codename')
    )
