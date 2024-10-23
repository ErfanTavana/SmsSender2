from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User  # Your custom User model

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(label="شماره تلفن", write_only=True)
    password = serializers.CharField(label="رمز عبور", write_only=True)
    token = serializers.CharField(label="توکن", read_only=True)
    user_id = serializers.UUIDField(label="شناسه کاربر", read_only=True)
    phone_number_display = serializers.CharField(label="نمایش شماره تلفن", read_only=True)
    first_name = serializers.CharField(label="نام", read_only=True)
    last_name = serializers.CharField(label="نام خانوادگی", read_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if not phone_number or not password:
            raise serializers.ValidationError('شماره تلفن و رمز عبور هر دو مورد نیاز هستند.')

        # Using the default authenticate method
        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            raise serializers.ValidationError('شماره تلفن یا رمز عبور اشتباه است.')

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return {
            'Authorization': f'Token {token.key}',
            'user_id': user.id,
            'phone_number_display': user.phone_number,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
