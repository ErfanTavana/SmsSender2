from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GroupSerializer, ContactSerializer
from SmsSender2.utils import normalize_phone_number
from contacts.models import Contact
from organizations.models import Group
from .utils import check_user_organization


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
            serializer.save(created_by=user, organization=organization_user)
            return Response({
                'message': 'مخاطب با موفقیت ایجاد شد.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        # پردازش خطاها برای استخراج اولین پیام خطا
        first_error_message = next(iter(serializer.errors.values()))[0]

        return Response({
            'message': first_error_message,  # اولین پیام خطا به عنوان رشته در message
            'data': serializer.errors  # نگهداری همه خطاها در data
        }, status=status.HTTP_400_BAD_REQUEST)