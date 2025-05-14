
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Device
from .serializers import DeviceLogSerializer


class DeviceLogCreateAPIView(APIView):
    """
    API برای ثبت یک یا چند لاگ برای دستگاه خاص
    """
    def post(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = DeviceLogSerializer(data=request.data, many=is_many)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Log(s) created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
