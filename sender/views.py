# views.py
from django.shortcuts import render, redirect
from django.views import View
from .models import Message, Group, User

from django.shortcuts import render, redirect
from django.views import View
from .models import SmsProgram
from text_messages.models import Message
from accounts.models import User
from organizations.models import Group

import random
from django.shortcuts import render, redirect
from django.views import View
from .models import SmsProgram, UserTask
from text_messages.models import Message
from accounts.models import User
from organizations.models import Group
from contacts.models import Contact  # فرض بر این است که Contact مدل مخاطب است
from django.shortcuts import render, get_object_or_404, redirect


class CreateSmsProgramView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        organization = request.user.organization

        # واکشی داده‌ها برای نمایش در انتخاب‌گرها
        messages = Message.objects.filter(organization_id=organization.id)
        groups = Group.objects.filter(organization_id=organization.id)
        users = User.objects.filter(organization_id=organization.id)

        return render(request, 'sender/sms_program_create.html', {
            'messages': messages,
            'groups': groups,
            'users': users,
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        # دریافت داده‌ها از درخواست
        sms_program_name = request.POST.get('sms_program_name')
        selected_message_id = request.POST.get('selected_message')
        selected_group_ids = request.POST.getlist('selected_groups')
        selected_user_ids = request.POST.getlist('selected_users')
        organization = request.user.organization

        # اعتبارسنجی ساده برای اطمینان از پر بودن نام برنامه
        if not sms_program_name:
            return render(request, 'sender/sms_program_create.html', {
                'message': 'نام برنامه پیامکی الزامی است.',
                'error': True,
                'messages': Message.objects.filter(organization_id=organization.id),
                'groups': Group.objects.filter(organization_id=organization.id),
                'users': User.objects.filter(organization_id=organization.id),
            })

        # بررسی و واکشی پیام انتخاب‌شده، گروه‌ها و کاربران
        selected_message = Message.objects.filter(organization_id=organization.id, id=selected_message_id).first()
        selected_groups = Group.objects.filter(organization_id=organization.id, id__in=selected_group_ids)
        selected_users = User.objects.filter(organization_id=organization.id, id__in=selected_user_ids)

        if not selected_message:
            return render(request, 'sender/sms_program_create.html', {
                'message': 'پیام انتخاب‌شده نامعتبر است.',
                'error': True,
                'messages': Message.objects.filter(organization_id=organization.id),
                'groups': Group.objects.filter(organization_id=organization.id),
                'users': User.objects.filter(organization_id=organization.id),
            })

        # ذخیره برنامه پیامکی
        sms_program = SmsProgram.objects.create(
            name=sms_program_name,
            message=selected_message,
            organization=organization
        )

        # اضافه کردن گروه‌ها و کاربران انتخاب‌شده به برنامه
        sms_program.groups.set(selected_groups)
        sms_program.users.set(selected_users)
        sms_program.save()

        # دریافت کل مخاطبین زیرمجموعه گروه‌های انتخاب‌شده
        contacts = Contact.objects.filter(groups__in=selected_groups).distinct()

        # تقسیم مخاطبین به صورت تصادفی بین کاربران انتخابی
        contact_list = list(contacts)
        random.shuffle(contact_list)  # تصادفی کردن لیست مخاطبین
        num_users = len(selected_users)

        # ایجاد تسک برای هر کاربر و تقسیم مخاطبین
        for i, user in enumerate(selected_users):
            # مخاطبین تخصیص‌یافته به این کاربر
            user_contacts = contact_list[i::num_users]  # تقسیم لیست به بخش‌های مساوی

            # ایجاد تسک برای کاربر
            user_task = UserTask.objects.create(
                sms_program=sms_program,
                organization=organization,
                assigned_user=user
            )
            user_task.contacts.set(user_contacts)  # تخصیص مخاطبین به تسک
            user_task.save()

        return redirect('sms_program_list')



class SmsProgramListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        # واکشی لیست برنامه‌های پیامکی
        sms_programs = SmsProgram.objects.filter(organization=request.user.organization)

        return render(request, 'sender/sms_program_list.html', {
            'sms_programs': sms_programs
        })


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import SmsProgram
from text_messages.models import Message
from accounts.models import User
from organizations.models import Group


from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import SmsProgram, UserTask
from contacts.models import Contact
from text_messages.models import Message
from accounts.models import User
from organizations.models import Group

class SmsProgramEditView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')

        organization = request.user.organization
        sms_program = get_object_or_404(SmsProgram, pk=pk, organization=organization)

        # واکشی داده‌های مورد نیاز برای فرم ویرایش
        messages = Message.objects.filter(organization_id=organization.id)
        groups = Group.objects.filter(organization_id=organization.id)
        users = User.objects.filter(organization_id=organization.id)

        return render(request, 'sender/sms_program_edit.html', {
            'sms_program': sms_program,
            'messages': messages,
            'groups': groups,
            'users': users,
        })

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')

        organization = request.user.organization
        sms_program = get_object_or_404(SmsProgram, pk=pk, organization=organization)

        # دریافت داده‌ها از فرم
        sms_program.name = request.POST.get('sms_program_name')
        selected_message_id = request.POST.get('selected_message')
        selected_group_ids = request.POST.getlist('selected_groups')
        selected_user_ids = request.POST.getlist('selected_users')

        # اعتبارسنجی و واکشی پیام مرتبط
        selected_message = Message.objects.filter(organization_id=organization.id, id=selected_message_id).first()
        if not selected_message:
            return render(request, 'sender/sms_program_edit.html', {
                'sms_program': sms_program,
                'messages': Message.objects.filter(organization_id=organization.id),
                'groups': Group.objects.filter(organization_id=organization.id),
                'users': User.objects.filter(organization_id=organization.id),
                'error': 'پیام انتخاب شده نامعتبر است.',
            })

        # ذخیره‌سازی داده‌های جدید
        sms_program.message = selected_message
        sms_program.groups.set(Group.objects.filter(id__in=selected_group_ids, organization_id=organization.id))
        sms_program.users.set(User.objects.filter(id__in=selected_user_ids, organization_id=organization.id))
        sms_program.save()

        # بروزرسانی وظایف
        all_contacts = Contact.objects.filter(groups__in=selected_group_ids).distinct()
        tasks = UserTask.objects.filter(sms_program=sms_program)

        # حذف مخاطبینی که دیگر در گروه‌های برنامه نیستند
        for task in tasks:
            task.contacts.remove(*[contact for contact in task.contacts.all() if contact.groups.first().id not in selected_group_ids])

        # تقسیم دوباره مخاطبین بین وظایف
        for idx, contact in enumerate(all_contacts):
            assigned_user = sms_program.users.all()[idx % sms_program.users.count()]
            task, created = UserTask.objects.get_or_create(sms_program=sms_program, assigned_user=assigned_user, organization=organization)
            task.contacts.add(contact)

        return redirect('sms_program_list')



class SmsProgramDeleteView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')

        # پیدا کردن و حذف برنامه پیامکی
        sms_program = get_object_or_404(SmsProgram, pk=pk, organization=request.user.organization)
        sms_program.delete()
        return redirect('sms_program_list')
