from django.shortcuts import render, redirect
from .models import Group, Organization

from django.shortcuts import render, redirect
from .models import Group, Organization
from django.views import View


class CreateGroup(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'organization/group_create.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        organization = request.user.organization

        # بررسی عدم وجود گروه با همین نام در همان سازمان
        if Group.objects.filter(name=name, organization=organization).exists():
            return render(request, 'organization/group_create.html', {
                'message': 'گروهی با این نام در این سازمان قبلاً ثبت شده است.',
                'error': True
            })
        Group.objects.create(name=name, organization=organization, description=description)

        return redirect('group_list')


from django.shortcuts import render, redirect
from django.views import View
from .models import Group


class GroupListView(View):
    def get(self, request):
        # بررسی اینکه کاربر لاگین کرده است
        if not request.user.is_authenticated:
            return redirect('login')

        # واکشی تمامی گروه‌ها
        groups = Group.objects.filter(organization=request.user.organization)

        # ارسال لیست گروه‌ها به قالب
        return render(request, 'organization/group_list.html', {'data': {'groups': groups}})


from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Group


class EditGroupView(View):
    def get(self, request, group_id):
        if not request.user.is_authenticated:
            return redirect('login')

        # دریافت گروه با استفاده از شناسه و بررسی وجود آن
        group = get_object_or_404(Group, id=group_id, organization=request.user.organization)

        # ارسال اطلاعات گروه به قالب برای پر کردن فرم
        return render(request, 'organization/group_edit.html', {'group': group})

    def post(self, request, group_id):
        if not request.user.is_authenticated:
            return redirect('login')
        # دریافت گروه و به‌روزرسانی اطلاعات
        group = get_object_or_404(Group, id=group_id, organization=request.user.organization)

        name = request.POST.get('name')
        description = request.POST.get('description')

        # بررسی عدم وجود گروه با همین نام در همان سازمان (به جز گروه جاری)
        if Group.objects.filter(name=name, organization=group.organization).exclude(id=group_id).exists():
            return render(request, 'organization/group_edit.html', {
                'group': group,
                'message': 'گروهی با این نام در این سازمان قبلاً ثبت شده است.',
                'error': True
            })

        # به‌روزرسانی اطلاعات گروه
        group.name = name
        group.description = description
        group.save()

        return redirect('group_list')


from django.shortcuts import redirect, get_object_or_404
from django.views import View
from .models import Group


class DeleteGroupView(View):
    def get(self, request, group_id):
        if not request.user.is_authenticated:
            return redirect('login')

        # دریافت گروه با استفاده از شناسه و بررسی وجود آن
        group = get_object_or_404(Group, id=group_id, organization=request.user.organization)

        # حذف گروه
        group.delete()

        # بازگشت به صفحه لیست گروه‌ها پس از حذف
        return redirect('group_list')