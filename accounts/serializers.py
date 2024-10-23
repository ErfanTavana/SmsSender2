from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User  # مدل کاربر شما

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, label="رمز عبور")
    token = serializers.CharField(read_only=True, label="توکن")
    user_id = serializers.IntegerField(read_only=True, label="شناسه کاربر")
    phone_number_display = serializers.CharField(read_only=True, label="نمایش شماره تلفن")
    first_name = serializers.CharField(read_only=True, label="نام")
    last_name = serializers.CharField(read_only=True, label="نام خانوادگی")

    class Meta:
        model = User
        fields = ['phone_number', 'password', 'token', 'user_id', 'phone_number_display', 'first_name', 'last_name']

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if not phone_number or not password:
            raise serializers.ValidationError('شماره تلفن و رمز عبور هر دو مورد نیاز هستند.')

        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            raise serializers.ValidationError('شماره تلفن یا رمز عبور اشتباه است.')

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return {
            'token': token.key,
            'user_id': user.id,
            'phone_number_display': user.phone_number,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
