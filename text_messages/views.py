from django.template.context_processors import request
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Message
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from organizations.models import Group


class MessageListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        messages = Message.objects.filter(organization_id=request.user.organization.id)
        return render(request, 'text_messages/message_list.html', {'messages': '', 'data': {'messages': messages}})


class MessagesCreateView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        groups = Group.objects.filter(organization=request.user.organization)

        return render(request, 'text_messages/messages_create.html', {'groups': groups})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        text = request.POST.get('text')
        message_type = request.POST.get('message_type')
        is_approved = request.POST.get('is_approved') == 'on'
        selected_group_ids = request.POST.getlist('selected_groups')  # دریافت گروه‌های انتخاب شده

        # ایجاد یک پیام جدید
        new_message = Message.objects.create(
            text=text,
            organization=request.user.organization,
            created_by=request.user,
            message_type=message_type,
            is_approved=is_approved
        )

        # اضافه کردن گروه‌ها به پیام
        new_message.groups.set(Group.objects.filter(id__in=selected_group_ids, organization=request.user.organization))
        new_message.save()

        return redirect('message_list')


class EditMessageView(View):
    def get(self, request, message_id):
        if not request.user.is_authenticated:
            return redirect('login')
        message = get_object_or_404(Message, id=message_id, organization_id=request.user.organization.id)
        groups = Group.objects.filter(organization=request.user.organization)  # گروه‌ها را واکشی کنید
        selected_groups = message.groups.all()  # گروه‌های انتخاب شده

        return render(request, 'text_messages/edit_message.html', {
            'message': message,
            'groups': groups,
            'selected_groups': selected_groups  # گروه‌های انتخاب شده را به قالب ارسال کنید
        })

    def post(self, request, message_id):
        if not request.user.is_authenticated:
            return redirect('login')
        message = get_object_or_404(Message, id=message_id, organization_id=request.user.organization.id)

        # دریافت داده‌های فرم
        text = request.POST.get('text')
        message_type = request.POST.get('message_type')
        is_approved = request.POST.get('is_approved') == 'on'  # تبدیل به بولین
        selected_group_ids = request.POST.getlist('selected_groups')  # دریافت گروه‌های انتخاب شده

        # به‌روزرسانی ویژگی‌های پیام
        message.text = text
        message.message_type = message_type
        message.is_approved = is_approved
        message.save()

        # بروزرسانی گروه‌ها
        message.groups.set(Group.objects.filter(id__in=selected_group_ids, organization=request.user.organization))

        return redirect('message_list')

class DeleteMessageView(View):
    def get(self, request, message_id):
        if not request.user.is_authenticated:
            return redirect('login')

        # پیدا کردن پیام با استفاده از id
        message = get_object_or_404(Message, id=message_id, organization_id=request.user.organization.id)

        # حذف پیام
        message.delete()
        return redirect('message_list')
