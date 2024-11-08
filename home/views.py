from django.views import View
from django.shortcuts import render, redirect

from django.utils import timezone
from django.db.models import Count, Q
from contacts.models import Contact
from organizations.models import Group
from datetime import timedelta


class ContactDashboardView(View):
    def get(self, request):
        # بررسی دسترسی کاربر به سازمان
        if not request.user.is_authenticated:
            return redirect('login')

        # محدود کردن مخاطبین به سازمان کاربر جاری
        user = request.user
        contacts = Contact.objects.filter(organization=user.organization)

        # توزیع مخاطبین بر اساس جنسیت
        male_count = contacts.filter(gender='مرد').count()
        female_count = contacts.filter(gender='زن').count()

        # توزیع مخاطبین بر اساس تاریخ ایجاد برای شش ماه اخیر
        creation_dates = []
        creation_counts = []
        for i in range(5, -1, -1):
            date = timezone.now() - timedelta(weeks=4 * i)
            count = contacts.filter(created_at__year=date.year, created_at__month=date.month).count()
            creation_dates.append(date.strftime("%Y-%m"))
            creation_counts.append(count)

        # توزیع گروهی مخاطبین
        groups = Group.objects.filter(contacts__organization=user.organization).annotate(count=Count('contacts'))
        group_names = [group.name for group in groups]
        group_counts = [group.count for group in groups]

        # توزیع مخاطبین بر اساس سازمان
        organization_names = [user.organization.name]
        organization_counts = [contacts.count()]

        # توزیع جنسیت و گروه
        male_group_counts = []
        female_group_counts = []
        for group in groups:
            male_group_counts.append(group.contacts.filter(gender='مرد').count())
            female_group_counts.append(group.contacts.filter(gender='زن').count())

        # تعداد مخاطبین ایجاد شده توسط کاربران
        user_creation_counts = contacts.values('created_by__first_name', 'created_by__last_name').annotate(
            count=Count('id'))
        user_names = [f"{user['created_by__first_name']} {user['created_by__last_name']}" for user in
                      user_creation_counts]
        user_counts = [user['count'] for user in user_creation_counts]

        # ارسال اطلاعات به قالب
        context = {
            'male_count': male_count,
            'female_count': female_count,
            'creation_dates': creation_dates,
            'creation_counts': creation_counts,
            'group_names': group_names,
            'group_counts': group_counts,
            'organization_names': organization_names,
            'organization_counts': organization_counts,
            'male_group_counts': male_group_counts,
            'female_group_counts': female_group_counts,
            'user_names': user_names,
            'user_counts': user_counts,
        }

        return render(request, 'home/index.html', context)
