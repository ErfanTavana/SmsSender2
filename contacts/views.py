from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GroupSerializer, ContactSerializer
from SmsSender2.utils import normalize_phone_number
from contacts.models import Contact
from organizations.models import Group
from .utils import check_user_organization
from text_messages.models import Message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse


class ContactApiView(APIView):
    def get(self, request):
        # استفاده از تابع کمکی
        error_response, user, organization_user = check_user_organization(request)
        if error_response:
            return error_response

        groups = user.groups.filter(organization=organization_user)

        if not groups:
            return Response({'message': 'شما هیچ گروهبندی تعریف نکرده‌اید.', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = GroupSerializer(groups, many=True)
        return Response(data={'message': 'گروه‌ها', 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        error_response, user, organization_user = check_user_organization(request)
        if error_response:
            return error_response

        # نرمال‌سازی شماره تلفن
        phone_number = request.data.get('phone_number')
        normalized_phone_number = normalize_phone_number(phone_number)

        # جستجوی مخاطب بر اساس شماره تلفن
        contact, created = Contact.objects.get_or_create(
            phone_number=normalized_phone_number,
            defaults={
                'created_by': user,
                'organization': organization_user,
            }
        )

        # اگر مخاطب وجود داشته باشد، اطلاعات آن را به‌روزرسانی کنید
        if not created:
            serializer = ContactSerializer(contact, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                contact = serializer.save()
                message = 'مخاطب با موفقیت به‌روزرسانی شد.'
            else:
                first_error_message = next(iter(serializer.errors.values()))[0]
                return Response({
                    'message': first_error_message,
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ContactSerializer(contact, data=request.data, context={'request': request})
            if serializer.is_valid():
                contact = serializer.save()
                message = 'مخاطب با موفقیت ایجاد شد.'
            else:
                first_error_message = next(iter(serializer.errors.values()))[0]
                return Response({
                    'message': first_error_message,
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        # دریافت گروه انتخابی از درخواست
        selected_groups = serializer.validated_data.get('groups', [])
        last_message = None

        if selected_groups:
            selected_group = selected_groups[0]
            last_message = Message.objects.filter(
                organization=organization_user,
                group_id=selected_group.id,
                message_type='فردی',
            ).order_by('-created_at').first()

        return Response({
            'message': message,
            'data': {
                'contact_info': serializer.data,
                'last_message': last_message.text if last_message else None
            }
        }, status=status.HTTP_200_OK)


class ContactsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'contacts/contacts_list.html')
