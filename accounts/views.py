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
        if request.user.is_authenticated:
            return redirect('contacts_list')
        return render(request, 'accounts/login.html')

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = authenticate(phone_number=phone_number, password=password)
        if user:
            login(request, user)
            return redirect('contacts_list')
        else:
            return render(request, 'accounts/login.html', {'message': 'نام کاربری یا رمز عبور نادرست است.', 'data': {}})
