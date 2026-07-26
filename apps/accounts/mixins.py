from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Usage:
        class TeacherDashboard(RoleRequiredMixin, TemplateView):
            allowed_roles = ["teacher", "admin"]
    """
    allowed_roles = []

    def test_func(self):
        return self.request.user.role in self.allowed_roles


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ["admin"]


class TeacherRequiredMixin(RoleRequiredMixin):
    allowed_roles = ["teacher", "admin"]