from import_export import resources
from .models import Contact


class ContactResource(resources.ModelResource):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'phone_number', 'gender', 'created_by', 'created_at')
        export_order = ('first_name', 'last_name', 'phone_number', 'gender', 'created_by', 'created_at')

    def before_export(self, queryset, data, *args, **kwargs):
        user = kwargs.get('user')
        if user is None:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            # در صورتی که user وجود ندارد، کل queryset را بر می‌گردانیم
            return queryset
        return queryset.filter(organization_id=user.organization.id)
