from rest_framework import serializers
from .models import (
    Company,
    Membership,
    Video
)

from .services import get_or_create_membership, create_company_by_user

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields= (
            'id', 'name','description','balance'
        )
        read_only_fields=('id',)


class MembershipSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    company_info = serializers.SerializerMethodField()
    company_id = serializers.IntegerField()

    class Meta:
        model = Membership
        fields= (
            'id','user_info', 'company_id','role', 'is_active','company_info'
        )
        read_only_fields=('id',)

    def get_user_info(self, obj):
        user = obj.user
        return {
            'id': user.id,
            'username': user.username,
        }

    def get_company_info(serf, obj):
        company = obj.company
        return {
            'id': company.id,
            'name': company.name,
        }
    

class MembershipUpdateSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=Membership.Roles.choices)
    is_active = serializers.BooleanField()
    company_id = serializers.IntegerField()

    class Meta:
        model = Membership
        fields = (
            'member_id', 'role', 'company_id', 'is_active'
        )

    def validate(self, attrs):
        try:
            target_member = Membership.objects.get(id=attrs['member_id'])
        except:
            raise serializers.ValidationError('member is not exist')

        if target_member.company.id != attrs['company_id']:
            raise serializers.ValidationError('company_id and member company is not match')

        attrs['target_member'] = target_member
        return attrs


class VideoSerializer(serializers.ModelSerializer):
    member_info = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    link = serializers.CharField()
    company_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Video
        fields = (
            'id','member_info','user_info', 'link','date','company_id'
        )
        read_only_fields= (
            'id',
        )

    def get_user_info(self,obj):
        user = obj.member.user
        return {
            'id' : user.id,
            'username': user.username
        }

    def get_member_info(self,obj):
        member = obj.member
        return {
            'id': member.id,
            'role': member.role,
            'is_active': member.is_active
        }
    
    def validate_link(self,value):
        if 'http://' in value or 'https://' in value:
            return value
        else:
            raise serializers.ValidationError({'details': 'invalid link'})
    

class VideoUpdateSerializer(serializers.ModelSerializer):
    solution = serializers.ChoiceField(Video.Solution.choices)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Video
        fields = (
            'id','solution', 'member', 'date','company_id'
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance