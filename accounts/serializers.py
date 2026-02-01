from rest_framework import serializers
from models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True) #validators = [validate_password]
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username','email','first_name', 
                  'second_name', 'password', 'password_confirm')
        
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({'password': 'password and confirm_password is dont match'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(*validated_data)
        return user
    

class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        if email and password:
            user = authenticate(
                self.context.get('request'),
                username=email,
                password=password
            )
            if user:
                attrs['user'] = user
                return attrs
            else:
                raise ValueError('email or password is incorrect')

        else:
            raise serializers.ValidationError('required email and password')
        

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name','second_name'
        )
        read_only_fields = ('id', )


class UserUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('first_name', 'second_name')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    

class UserChangePasswordSerializer(serializers.Serializer):
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

