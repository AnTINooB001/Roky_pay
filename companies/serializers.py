from rest_framework import serializers
from . import models as comp_models

from .services import get_or_create_membership, create_company_by_user

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=comp_models.Companies
        fields= (
            'id', 'name','description','balance'
        )
        read_only_fields=('id',)

    def create(self,validated_data):
        try:
            company, _ = create_company_by_user(
                self.context['request'].user.id,
                **validated_data
            )
        except Exception as e:
            raise serializers.ValidationError({'details': str(e)})
        return company


class MembershipSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    company_info = serializers.SerializerMethodField()
    company_id = serializers.IntegerField()

    class Meta:
        model = comp_models.Memberships
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
    

    def create(self,validated_data):
        user = self.context.get('request').user
        company_id = validated_data.get('company_id')
        validated_data.pop('company_id')

        instance, created = get_or_create_membership(user_id=user.id,
                                                     company_id=company_id,
                                                     allow_create=True,
                                                     **validated_data)
        return instance, created
    

class MembershipUpdateSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=comp_models.Memberships.Roles.choices)
    is_active = serializers.BooleanField()
    company_id = serializers.IntegerField()

    class Meta:
        model = comp_models.Memberships
        fields = (
            'member_id', 'role', 'company_id', 'is_active'
        )

    def validate(self, attrs):
        target_member = comp_models.Memberships.objects.get(id=attrs['member_id'])
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
        model = comp_models.Video
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
    solution = serializers.ChoiceField(comp_models.Video.Solution.choices)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = comp_models.Video
        fields = (
            'id','solution', 'member', 'date','company_id'
        )


    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance