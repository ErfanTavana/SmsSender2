
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Device
from .serializers import DeviceLogSerializer
from contacts.views import get_request_data


class DeviceLogCreateAPIView(APIView):
    """
    API برای ثبت لیستی از لاگ‌ها برای یک دستگاه
    """

    def post(self, request, *args, **kwargs):
        data = get_request_data(request)

        device_uid = data.get("device_uid")
        logs = data.get("logs")

        if not device_uid or not isinstance(logs, list):
            return Response({"error": "device_uid and logs (as list) are required."}, status=400)

        device, _ = Device.objects.get_or_create(uid=device_uid)

        for log in logs:
            log["device"] = device.uid  # 👈 چون SlugRelatedField بر اساس uid است

        serializer = DeviceLogSerializer(data=logs, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"{len(logs)} log(s) created successfully"}, status=201)

        return Response(serializer.errors, status=400)


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ReceivedSMS

class ReceiveSMSAPIView(APIView):
    """
    API برای دریافت پیامک‌های دریافتی از سامانه پیامکی (POST)
    """

    def post(self, request, *args, **kwargs):
        sender = request.data.get('from')
        receiver = request.data.get('to')
        message = request.data.get('message')

        if not sender or not receiver or not message:
            return Response({
                "error": "پارامترهای from, to, message الزامی هستند."
            }, status=status.HTTP_400_BAD_REQUEST)

        ReceivedSMS.objects.create(
            sender=sender,
            receiver=receiver,
            message=message
        )

        return Response({"message": "پیام با موفقیت ذخیره شد."}, status=status.HTTP_201_CREATED)
