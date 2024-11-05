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

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Contact
from .serializers import ContactSerializer, GroupSerializer
from organizations.models import Group
from SmsSender2.utils import normalize_phone_number

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Contact
from .serializers import ContactSerializer, GroupSerializer
from organizations.models import Group
from SmsSender2.utils import normalize_phone_number


class GroupListApiView(APIView):
    def get(self, request):
        error_response, user, organization_user = check_user_organization(request)
        if error_response:
            return error_response

        groups = user.groups.filter(organization=organization_user)

        if not groups:
            return Response({'message': 'شما هیچ گروهبندی تعریف نکرده‌اید.', 'data': {}},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = GroupSerializer(groups, many=True)
        return Response(data={'message': 'گروه‌ها', 'data': serializer.data}, status=status.HTTP_200_OK)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Contact
from .serializers import ContactSerializer
from organizations.models import Group
from SmsSender2.utils import normalize_phone_number

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Contact
from .serializers import ContactSerializer
from organizations.models import Group
from SmsSender2.utils import normalize_phone_number

class ContactCreateApiView(APIView):
    def post(self, request):
        # بررسی دسترسی کاربر و سازمان
        error_response, user, organization_user = check_user_organization(request)
        if error_response:
            return error_response

        # دریافت داده‌های مخاطبین از درخواست
        contacts_data = request.data.get('contacts', [])
        if not contacts_data:
            return Response({
                'message': 'هیچ مخاطبی ارسال نشده است.',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        created_contacts = []
        for contact_data in contacts_data:
            # نرمال‌سازی شماره تلفن
            phone_number = contact_data.get('phone_number')
            normalized_phone_number = normalize_phone_number(phone_number)

            # جستجو یا ایجاد مخاطب بر اساس شماره تلفن
            contact, created = Contact.objects.get_or_create(
                phone_number=normalized_phone_number,
                defaults={'created_by': user, 'organization': organization_user}
            )

            # اگر groups به صورت رشته ارسال شود، آن را به لیست تبدیل می‌کنیم
            group_data = contact_data.get('groups', [])
            if isinstance(group_data, str):
                group_data = [group_data]

            # اگر مخاطب جدید باشد، آن را ایجاد می‌کنیم
            if created:
                serializer = ContactSerializer(contact, data=contact_data, context={'request': request})
                if serializer.is_valid():
                    contact = serializer.save()
                    contact.groups.set(group_data)  # گروه‌ها را به مخاطب اضافه می‌کنیم
                    created_contacts.append({'contact_info': serializer.data, 'message': 'مخاطب با موفقیت ایجاد شد.'})
                else:
                    # در صورت وجود خطا در اعتبارسنجی، پیام خطا را برمی‌گردانیم
                    first_error_message = next(iter(serializer.errors.values()))[0]
                    return Response({
                        'message': first_error_message,
                        'data': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # اگر مخاطب وجود داشته باشد، اطلاعات آن را به‌روزرسانی می‌کنیم
                serializer = ContactSerializer(contact, data=contact_data, partial=True, context={'request': request})
                if serializer.is_valid():
                    contact = serializer.save()
                    contact.groups.set(group_data)  # گروه‌ها را به‌روزرسانی می‌کنیم
                    created_contacts.append({'contact_info': serializer.data, 'message': 'مخاطب با موفقیت به‌روزرسانی شد.'})
                else:
                    # در صورت وجود خطا در اعتبارسنجی، پیام خطا را برمی‌گردانیم
                    first_error_message = next(iter(serializer.errors.values()))[0]
                    return Response({
                        'message': first_error_message,
                        'data': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)

        # در نهایت، پاسخ موفقیت‌آمیز با اطلاعات مخاطبین ایجاد شده
        return Response({
            'message': 'مخاطبین با موفقیت پردازش شدند.',
            'data': created_contacts
        }, status=status.HTTP_200_OK)

class ContactsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        return render(request, 'contacts/contacts_list.html')
