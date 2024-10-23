from rest_framework import serializers
from organizations.models import Group
from .models import Contact
from SmsSender2.utils import normalize_phone_number
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone_number', 'gender', 'groups']

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
                raise serializers.ValidationError(f"شما به گروه '{group.name}' دسترسی ندارید.")

        return groups

    def create(self, validated_data):
        """
        Add created_by and organization fields automatically.
        """
        validated_data['created_by'] = self.context['request'].user
        validated_data['organization'] = self.context['request'].user.organization
        return super().create(validated_data)