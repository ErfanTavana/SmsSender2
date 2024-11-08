from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class SMSProgramAccessRequiredMixin:
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # چک کردن دسترسی کاربر
        if not request.user.can_access_sms_program:
            raise PermissionDenied("شما مجاز به دسترسی به این صفحه نیستید.")
        return super().dispatch(request, *args, **kwargs)


class BulkSMSAccessRequiredMixin:
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # Check if the user has access to send bulk SMS
        if not request.user.can_send_bulk_sms:
            raise PermissionDenied("شما مجاز به دسترسی به این صفحه نیستید.")
        return super().dispatch(request, *args, **kwargs)
