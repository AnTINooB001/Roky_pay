from .models import (
    Company,
    Membership,
    Video
)
from django.contrib.auth import get_user_model
from django.db import transaction
from typing import Optional 


def get_or_create_membership(user_id,company_id,allow_create,**other_data):
    if allow_create:
        return Membership.objects.get_or_create(
            user_id = user_id,
            company_id=company_id,
            defaults=other_data
        )
    else:
        instance = Membership.objects.filter(user_id=user_id,
                                                            company_id=company_id).first()
        return instance, False


def get_video_to_review(admin_member: Membership) -> Optional[Video]:
    """Возвращает video для оценки admin'ом или
                  None если видео для оценки отсутствует"""
    
    if admin_member is None or admin_member.role != Membership.Roles.Admin:
        return None
    
    video = Video.objects.filter(
        admin=admin_member).filter(
            solution=Video.Solution.Wait
            ).first()
    if video:
        return video
    
    with transaction.atomic():
        video = Video.objects.filter(
            member__company_id=admin_member.company.id,
            admin__isnull=True
            ).select_for_update(skip_locked=True).first()
        if video:
            video.admin = admin_member
            video.save()
            return video
        
    return None


def create_video_by_user(link, user_id,company_id):

    member = Membership.objects.filter(user_id=user_id,company_id=company_id).first()
    if member.role != Membership.Roles.User:
        return False
    video = Video(member=member,link=link)
    video.save()
    return video
    

def get_user_video_history(member_id):
    member = Membership.objects.filter(pk=member_id).first()
    return Video.objects.all().filter(member=member).values_list()


def create_company_by_user(user_id, **company_data):
    with transaction.atomic():
        new_company = Company.objects.create(**company_data)

        member = Membership.objects.create(
            user_id=user_id, 
            company=new_company, 
            role=Membership.Roles.SuperAdmin
        )
        return new_company, member


