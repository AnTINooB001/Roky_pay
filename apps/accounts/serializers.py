from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """ Сериализатор для регистрации пользователя """
    password = serializers.CharField(write_only=True) #validators = [validate_password]
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username','first_name', 
                  'second_name', 'password', 'confirm_password',)
        
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({'password': 'password and confirm_password is dont match'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
    

class UserLoginSerializer(serializers.Serializer):
    """ Сериализатор для входа пользователя """
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']

        if username and password:
            user = authenticate(
                self.context.get('request'),
                username=username,
                password=password
            )
            if user:
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('username or password is incorrect')

        else:
            raise serializers.ValidationError('required username and password')
        

class UserProfileSerializer(serializers.ModelSerializer):
    """ Сериализоатор для профиля пользователя """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name','second_name', 'full_name'
        )
        read_only_fields = ('id', )


class UserUpdateSerializer(serializers.ModelSerializer):
    """ Сериализатор для обновления данных пользователя """
    class Meta:
        fields = ('first_name', 'second_name')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserChangePasswordSerializer(serializers.Serializer):
    """ Сериализатор для изменения пароля пользователя"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_passowrd_confirm = serializers.CharField(write_only=True)


    def validate_old_password(self, value):
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError('old password is incorrect')
        return value
    

    def validate(self, attrs):
        new_password = attrs['new_password']
        if new_password != attrs['new_passowrd_confirm']:
            raise serializers.ValidationError('New password and confirm password in not match')
        else:
            return attrs
        
        
    def save(self):
        user = self.context.get('request').user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

