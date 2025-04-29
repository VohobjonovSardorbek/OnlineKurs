from rest_framework.serializers import ModelSerializer
from .models import *


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Account(**validated_data)
        user.set_password(password)

        if user.role.lower() == 'student':
            user.is_staff = False
        else:
            user.is_staff = True

        user.save()


        return user

class StudentSerializer(ModelSerializer):
    user = AccountSerializer()

    class Meta:
        model = Student
        fields = '__all__'

        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'joined_at': {
                'read_only': True
            }
        }

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for key, value in user_data.items():
                setattr(instance.user, key, value)
            instance.user.save()

        return super().update(instance, validated_data)
