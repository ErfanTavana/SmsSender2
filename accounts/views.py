from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from organizations.models import Group
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()
from django.contrib.auth.hashers import make_password


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


from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from organizations.models import Group  # فرض کنید مدل Group اینجا تعریف شده است

User = get_user_model()


class UserCreateView(View):
    def get(self, request):
        # فیلتر کردن گروه‌ها بر اساس سازمان کاربر
        groups = Group.objects.filter(organization_id=request.user.organization.id)

        return render(request, 'accounts/user_create.html', {
            'message': '',
            'data': {
                'groups': groups,
                'selected_groups': []  # در ابتدا گروه‌های انتخابی خالی است
            }
        })

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        groups = request.POST.getlist('group')

        # بررسی وجود کاربر با شماره تلفن وارد شده
        if User.objects.filter(phone_number=phone_number).exists():
            groups_queryset = Group.objects.filter(organization_id=request.user.organization.id)
            # ارسال پیام خطا به قالب
            return render(request, 'accounts/user_create.html', {
                'message': "کاربری با این شماره تلفن از قبل وجود دارد.",
                'data': {
                    'groups': groups_queryset,
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': phone_number,
                    'selected_groups': [int(g) for g in groups],
                }
            })

        # ساخت کاربر جدید با استفاده از create_user
        new_user = User.objects.create_user(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            organization_id=request.user.organization.id,
            password=password
        )

        # فیلتر کردن گروه‌های معتبر برای اطمینان از تعلق به سازمان کاربر
        valid_groups = Group.objects.filter(id__in=groups, organization_id=request.user.organization.id).values_list(
            'id', flat=True)

        # تنظیم گروه‌های معتبر برای کاربر جدید
        new_user.groups.set(valid_groups)

        return redirect('user_list')


class UserListView(View):
    def get(self, request):
        users = User.objects.filter(
            organization_id=request.user.organization.id)  # می‌توانید فیلترهای بیشتری برای کاربران اضافه کنید
        return render(request, 'accounts/user_list.html', {'message': '', 'data': {'users': users}})


class UserEditView(View):
    def get(self, request, user_id):
        # یافتن کاربر با شناسه مشخص
        user = get_object_or_404(User, id=user_id)

        # انتخاب گروه‌ها بر اساس سازمان کاربر وارد شده
        groups = Group.objects.filter(organization_id=request.user.organization.id)

        # یافتن گروه‌های انتخاب شده توسط کاربر
        selected_groups = user.groups.values_list('id', flat=True)

        return render(request, 'accounts/user_edit.html', {
            'user': user,
            'groups': groups,
            'selected_groups': selected_groups
        })

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        # دریافت داده‌ها از فرم
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        groups = request.POST.getlist('group')

        # فیلتر کردن گروه‌ها برای اطمینان از اینکه به سازمان کاربر تعلق دارند
        valid_groups = Group.objects.filter(id__in=groups, organization_id=request.user.organization.id).values_list(
            'id', flat=True)

        # به‌روزرسانی اطلاعات کاربر
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.gender = gender
        user.groups.set(valid_groups)
        user.save()

        # انتقال به صفحه‌ی لیست کاربران یا نمایش پیغام موفقیت
        return redirect('user_list')


from django.http import HttpResponseForbidden


class UserDeleteView(View):
    def get(self, request, user_id):
        # جلوگیری از حذف خود کاربر
        users = User.objects.filter(
            organization_id=request.user.organization.id)  # می‌توانید فیلترهای بیشتری برای کاربران اضافه کنید
        if user_id == request.user.id:
            return render(request, 'accounts/user_list.html',
                          context={'message': 'شما نمی‌توانید خودتان را حذف کنید.', 'data': {'users': users}})

        # پیدا کردن کاربر مورد نظر و اطمینان از تعلق به سازمان کاربر درخواست‌دهنده
        user = get_object_or_404(User, id=user_id, organization_id=request.user.organization.id)

        # حذف کاربر
        user.delete()
        return redirect('user_list')
