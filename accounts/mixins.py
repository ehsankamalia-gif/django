from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(UserPassesTestMixin):
    """Allows Admins and Staff (anyone with is_staff=True). Blocks Customers."""

    def test_func(self):
        return self.request.user.is_staff


class SuperuserRequiredMixin(UserPassesTestMixin):
    """Admin-only. Used for views that manage staff roles/permissions."""

    def test_func(self):
        return self.request.user.is_superuser


class StaffPermissionRequiredMixin(StaffRequiredMixin, PermissionRequiredMixin):
    """Requires is_staff AND the specific permission(s) an Admin granted.

    Both checks are enforced even though in normal operation a user only
    ever holds a permission while they're staff (permissions are cleared
    on demotion) - this keeps the "staff status" and "granted access"
    checks independent so one can't silently cover for the other.
    """
