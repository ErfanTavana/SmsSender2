from .utils import check_user_organization

from .serializers import GroupSerializer
from django.db.models import Q  # اضافه کردن این خط
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ContactSerializer
from SmsSender2.utils import normalize_phone_number
from .models import Contact, Group
from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from .models import Contact

User = get_user_model()


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
                    created_contacts.append(
                        {'contact_info': serializer.data, 'message': 'مخاطب با موفقیت به‌روزرسانی شد.'})
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


class ContactCreateView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # کاربر باید وارد شود

        # گرفتن گروه‌ها برای انتخاب از جانب کاربر
        groups = Group.objects.filter(organization=request.user.organization)

        return render(request, 'contacts/contact_create.html', {'groups': groups})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # کاربر باید وارد شود

        # دریافت داده‌ها از فرم
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        selected_group_ids = request.POST.getlist('selected_groups')  # دریافت گروه‌های انتخابی

        # بررسی اعتبار داده‌ها (در صورت نیاز می‌توانید بررسی کنید)
        if not first_name or not last_name or not phone_number or not gender:
            return render(request, 'contacts/contact_create.html', {'message': 'تمامی فیلدها باید پر شوند.'})

        # ایجاد مخاطب جدید
        contact = Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            created_by=request.user,
            organization=request.user.organization
        )

        # اضافه کردن گروه‌ها به مخاطب
        contact.groups.set(Group.objects.filter(id__in=selected_group_ids, organization=request.user.organization))
        contact.save()

        # ارسال پیام موفقیت
        message = 'مخاطب با موفقیت ایجاد شد.'
        return render(request, 'contacts/contact_create.html',
                      {'message': message, 'groups': Group.objects.filter(organization=request.user.organization)})


from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Q  # برای جستجو
from .models import Contact

from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Q  # برای جستجو
from .models import Contact


class ContactListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # کاربر باید وارد شود

        # گرفتن نام جستجو از پارامترهای GET
        search_query = request.GET.get('search', '')

        # گرفتن مخاطبین مرتبط با سازمان کاربر و اعمال فیلتر بر اساس جستجو
        contacts = Contact.objects.filter(organization=request.user.organization)

        if search_query:
            # تقسیم رشته جستجو به نام و نام خانوادگی
            search_terms = search_query.split()  # تقسیم بر اساس فضا

            # ساخت فیلتر برای جستجو
            filters = Q()
            for term in search_terms:
                filters |= Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(
                    phone_number__icontains=term)

            contacts = contacts.filter(filters)

        return render(request, 'contacts/contact_list.html', {'contacts': contacts, 'search_query': search_query})


class ContactEditView(View):
    def get(self, request, contact_id):
        if not request.user.is_authenticated:
            return redirect('login')  # اگر کاربر وارد نشده باشد، به صفحه ورود هدایت می‌شود

        # پیدا کردن مخاطب با شناسه مشخص
        contact = get_object_or_404(Contact, id=contact_id, organization=request.user.organization)
        groups = Group.objects.filter(organization=request.user.organization)  # دریافت گروه‌ها برای انتخاب
        selected_groups = contact.groups.all()  # گروه‌های انتخاب شده

        return render(request, 'contacts/edit_contact.html', {
            'contact': contact,
            'groups': groups,
            'selected_groups': selected_groups  # ارسال گروه‌های انتخابی
        })

    def post(self, request, contact_id):
        if not request.user.is_authenticated:
            return redirect('login')  # اگر کاربر وارد نشده باشد، به صفحه ورود هدایت می‌شود

        contact = get_object_or_404(Contact, id=contact_id, organization=request.user.organization)

        # دریافت داده‌های فرم
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        selected_group_ids = request.POST.getlist('selected_groups')  # دریافت گروه‌های انتخابی

        # به‌روزرسانی مخاطب
        contact.first_name = first_name
        contact.last_name = last_name
        contact.phone_number = phone_number
        contact.gender = gender
        contact.save()

        # به‌روزرسانی گروه‌ها
        contact.groups.set(Group.objects.filter(id__in=selected_group_ids, organization=request.user.organization))

        return redirect('contact_list')  # هدایت به لیست مخاطبین بعد از ویرایش


class ContactDeleteView(View):
    def get(self, request, contact_id):
        if not request.user.is_authenticated:
            return redirect('login')  # اگر کاربر وارد نشده باشد به صفحه ورود هدایت شود

        # پیدا کردن مخاطب بر اساس شناسه
        contact = get_object_or_404(Contact, id=contact_id, organization=request.user.organization)

        # حذف مخاطب
        contact.delete()

        # بعد از حذف به لیست مخاطبین هدایت می‌کند
        return redirect('contact_list')  # نام URL لیست مخاطبین
