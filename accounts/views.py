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
from .mixins import UserAccessRequiredMixin

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


from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.views import View
from sender.models import UserTask  # فرض بر این است که مدل UserTask شامل تسک‌ها است


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
            # بررسی وجود تسک برای کاربر
            if UserTask.objects.filter(assigned_user=user).exists():
                return redirect('list_contacts_in_task_user')
            else:
                return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'message': 'نام کاربری یا رمز عبور نادرست است.', 'data': {}})


from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from organizations.models import Group  # فرض کنید مدل Group اینجا تعریف شده است

User = get_user_model()


class UserCreateView(UserAccessRequiredMixin, View):
    def get(self, request):
        # فیلتر کردن گروه‌ها بر اساس سازمان کاربر
        groups = Group.objects.filter(organization_id=request.user.organization.id)

        return render(request, 'accounts/user_create.html', {
            'message': '',
            'data': {
                'groups': groups,
                'selected_groups': [],  # در ابتدا گروه‌های انتخابی خالی است
                'access_controls': {  # دسترسی‌ها به صورت False به طور پیش‌فرض
                    'can_access_messages': False,
                    'can_access_users': False,
                    'can_access_groups': False,
                    'can_access_sms_program': False,
                    'can_access_contacts': False,
                    'can_send_bulk_sms': False,
                    'can_add_contacts': False
                }
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
            return render(request, 'accounts/user_create.html', {
                'message': "کاربری با این شماره تلفن از قبل وجود دارد.",
                'data': {
                    'groups': groups_queryset,
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': phone_number,
                    'selected_groups': [int(g) for g in groups],
                    'access_controls': {  # مقادیر دسترسی‌ها را از فرم دریافت می‌کنیم
                        'can_access_messages': request.POST.get('can_access_messages') == 'on',
                        'can_access_users': request.POST.get('can_access_users') == 'on',
                        'can_access_groups': request.POST.get('can_access_groups') == 'on',
                        'can_access_sms_program': request.POST.get('can_access_sms_program') == 'on',
                        'can_access_contacts': request.POST.get('can_access_contacts') == 'on',
                        'can_send_bulk_sms': request.POST.get('can_send_bulk_sms') == 'on',
                        'can_add_contacts': request.POST.get('can_add_contacts') == 'on',

                    }
                }
            })

        # ساخت کاربر جدید
        new_user = User.objects.create_user(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            organization_id=request.user.organization.id,
            password=password,
            # تنظیم دسترسی‌ها با استفاده از مقادیر دریافت‌شده از فرم
            can_access_messages=request.POST.get('can_access_messages') == 'on',
            can_access_users=request.POST.get('can_access_users') == 'on',
            can_access_groups=request.POST.get('can_access_groups') == 'on',
            can_access_sms_program=request.POST.get('can_access_sms_program') == 'on',
            can_access_contacts=request.POST.get('can_access_contacts') == 'on',
            can_send_bulk_sms=request.POST.get('can_send_bulk_sms') == 'on',
            can_add_contacts=request.POST.get('can_add_contacts') == 'on',

        )

        # تنظیم گروه‌های معتبر برای کاربر جدید
        valid_groups = Group.objects.filter(id__in=groups, organization_id=request.user.organization.id).values_list(
            'id', flat=True)
        new_user.groups.set(valid_groups)

        return redirect('user_list')


class UserListView(UserAccessRequiredMixin, View):
    def get(self, request):
        users = User.objects.filter(organization_id=request.user.organization.id)

        # تبدیل کاربران به لیست شامل اطلاعات دسترسی‌ها
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'gender': user.gender,
                'groups': user.groups.all(),
                'can_access_users': user.can_access_users,
                'can_access_groups': user.can_access_groups,
                'can_access_sms_program': user.can_access_sms_program,
                'can_access_contacts': user.can_access_contacts,
                'can_send_bulk_sms': user.can_send_bulk_sms,
            })

        return render(request, 'accounts/user_list.html', {'message': '', 'data': {'users': user_data}})


class UserEditView(UserAccessRequiredMixin, View):
    def get(self, request, user_id):
        # جلوگیری از ویرایش خود کاربر
        if user_id == request.user.id:
            return redirect('user_list')

        # یافتن کاربر با شناسه مشخص
        user = get_object_or_404(User, id=user_id)

        # انتخاب گروه‌ها بر اساس سازمان کاربر وارد شده
        groups = Group.objects.filter(organization_id=request.user.organization.id)

        # یافتن گروه‌های انتخاب شده توسط کاربر
        selected_groups = user.groups.values_list('id', flat=True)

        # دسترسی‌های کاربر
        access_controls = {
            'can_access_messages': user.can_access_messages,

            'can_access_users': user.can_access_users,
            'can_access_groups': user.can_access_groups,
            'can_access_sms_program': user.can_access_sms_program,
            'can_access_contacts': user.can_access_contacts,
            'can_send_bulk_sms': user.can_send_bulk_sms,
            'can_add_contacts': user.can_add_contacts,
        }

        return render(request, 'accounts/user_edit.html', {
            'user': user,
            'groups': groups,
            'selected_groups': selected_groups,
            'access_controls': access_controls
        })

    def post(self, request, user_id):
        # جلوگیری از ویرایش خود کاربر
        if user_id == request.user.id:
            return redirect('user_list')  # یا می‌توانید یک پیام خطا نمایش دهید

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

        # تنظیم دسترسی‌ها با استفاده از مقادیر دریافت‌شده از فرم
        user.can_access_messages = request.POST.get('can_access_messages') == 'on'
        user.can_access_users = request.POST.get('can_access_users') == 'on'
        user.can_access_groups = request.POST.get('can_access_groups') == 'on'
        user.can_access_sms_program = request.POST.get('can_access_sms_program') == 'on'
        user.can_access_contacts = request.POST.get('can_access_contacts') == 'on'
        user.can_send_bulk_sms = request.POST.get('can_send_bulk_sms') == 'on'
        user.can_add_contacts = request.POST.get('can_add_contacts') == 'on'

        user.save()

        # انتقال به صفحه‌ی لیست کاربران یا نمایش پیغام موفقیت
        return redirect('user_list')


class UserDeleteView(UserAccessRequiredMixin, View):
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
