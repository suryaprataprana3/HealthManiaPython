from rest_framework import serializers
from configurations.models import *
from django.shortcuts import get_object_or_404

class SignUpUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        print("validated_data",validated_data)
        user = super().create(validated_data)
        user.account_type = 'U'
        user.set_password(validated_data['password'])
        user.is_active = False
        user.otp_verified = False
        user.otp_creation()
        user.otp_send(user.otp,user.email)
        user.save()
        return user

    class Meta:
        model = Account
        fields = ['id', 'name', 'mobile','email','password']