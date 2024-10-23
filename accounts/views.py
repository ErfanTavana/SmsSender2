from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response({
                'data': data,
                'message': 'ورود با موفقیت انجام شد.'
            }, status=status.HTTP_200_OK)
        return Response({
            'data': {},
            'message': 'نام کاربری یا رمز عبور نادرست است.'
        }, status=status.HTTP_400_BAD_REQUEST)
