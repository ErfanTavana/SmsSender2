from rest_framework import serializers
from organizations.models import Group
from .models import Contact
from SmsSender2.utils import normalize_phone_number


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'sms_code']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone_number', 'gender', 'groups']
        read_only_fields = ['groups']

    def validate_phone_number(self, phone_number):
        """
        Validate and normalize the phone number to the standard Iranian format.
        """
        try:
            normalized_phone = normalize_phone_number(phone_number)
            if not normalized_phone:
                raise serializers.ValidationError("شماره تلفن نرمال‌سازی نشده است.")
            return normalized_phone
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_groups(self, groups):
        """
        Validate that the selected groups belong to the user's groups.
        """
        user = self.context['request'].user

        # دریافت گروه‌های مرتبط با کاربر
        user_groups = user.groups.all()

        # بررسی اینکه همه گروه‌های انتخابی توسط کاربر در گروه‌های کاربر موجود هستند
        for group in groups:
            if group not in user_groups:
                raise serializers.ValidationError(f"شما به گروه انتخابی دسترسی ندارید.")

        return groups

    def create(self, validated_data):
        """
        Add created_by and organization fields automatically.
        """
        validated_data['created_by'] = self.context['request'].user
        validated_data['organization'] = self.context['request'].user.organization
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Update contact information and groups.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)

        # به‌روزرسانی گروه‌ها
        new_groups = validated_data.get('groups', [])

        # افزودن گروه‌های جدید به لیست فعلی
        for group in new_groups:
            if group not in instance.groups.all():
                instance.groups.add(group)

        instance.save()
        return instance
