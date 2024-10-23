from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GroupSerializer, ContactSerializer
from SmsSender2.utils import normalize_phone_number
from contacts.models import Contact
from organizations.models import Group
from .utils import check_user_organization
from text_messages.models import Message


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
        # استفاده از تابع کمکی برای بررسی کاربر و سازمان
        error_response, user, organization_user = check_user_organization(request)
        if error_response:
            return error_response

        serializer = ContactSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            contact = serializer.save(created_by=user, organization=organization_user)

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
                'message': 'مخاطب با موفقیت ایجاد شد.',
                'data': {
                    'contact_info': serializer.data,
                    'last_message': last_message.text if last_message else None  # استفاده از ویژگی صحیح
                }
            }, status=status.HTTP_201_CREATED)

        # پردازش خطاها برای استخراج اولین پیام خطا
        first_error_message = next(iter(serializer.errors.values()))[0]

        return Response({
            'message': first_error_message,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
