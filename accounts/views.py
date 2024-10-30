from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
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

class LoginView(View):
    def get(self, request):
        # اگر کاربر لاگین باشد، او را به صفحه اصلی هدایت کنید
        if request.user.is_authenticated:
            return redirect('home')  # نام URL صفحه اصلی شما
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # نام URL صفحه اصلی
        else:
            return HttpResponse('نام کاربری یا رمز عبور نادرست است.')