from django.template.context_processors import request
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Message
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect


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

        return render(request, 'text_messages/messages_create.html')

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        text = request.POST.get('text')
        message_type = request.POST.get('message_type')
        is_approved = request.POST.get('is_approved') == 'on'

        # ایجاد یک پیام جدید
        new_message = Message.objects.create(
            text=text,
            organization=request.user.organization,
            created_by=request.user,
            message_type=message_type,
            is_approved=is_approved
        )
        new_message.save()
        return render(request, 'text_messages/messages_create.html',
                      {"message": 'پیام با موفقیت ثبت شد.', 'data': {'new_message': new_message}})


class EditMessageView(View):
    def get(self, request, message_id):
        if not request.user.is_authenticated:
            return redirect('login')
        message = get_object_or_404(Message, id=message_id, organization_id=request.user.organization.id)
        return render(request, 'text_messages/edit_message.html', {'message': message})

    def post(self, request, message_id):
        if not request.user.is_authenticated:
            return redirect('login')
        message = get_object_or_404(Message, id=message_id, organization_id=request.user.organization.id)
        # دریافت داده‌های فرم
        text = request.POST.get('text')
        message_type = request.POST.get('message_type')
        is_approved = request.POST.get('is_approved') == 'on'  # تبدیل به بولین

        # به‌روزرسانی ویژگی‌های پیام
        message.text = text
        message.message_type = message_type
        message.is_approved = is_approved
        message.save()

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
