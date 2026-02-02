from companies import models as comp_models
from django.contrib.auth import get_user_model
from typing import Optional 


def get_or_create_membership(user_id,company_id,allow_create,**other_data):
    if allow_create:
        return comp_models.Memberships.objects.get_or_create(
            user_id = user_id,
            company_id=company_id,
            defaults=other_data
        )
    else:
        instance = comp_models.Memberships.objects.filter(user_id=user_id,
                                                            company_id=company_id).first()
        return instance, False


def get_video_to_review(user_id,company_id) -> Optional[comp_models.Video]:
    """Возвращает video для оценки admin'ом или
                  None если видео для оценки отсутствует"""
    admin_member = comp_models.Memberships.objects.filter(user_id=user_id,company_id=company_id).first()
    if admin_member is None or admin_member.role != comp_models.Memberships.Roles.Admin:
        return None
    solutions = comp_models.Video.Solution
    video = comp_models.Video.objects.filter(admin=admin_member).filter(solution=solutions.Wait).first()
    if video is None:
        video = comp_models.Video.objects.filter(member__company_id=company_id).filter(admin=None).first()
        if video is None:
            return None
        video.admin = admin_member
        video.save()
    return video


def create_video_by_user(link, user_id,company_id):

    member = comp_models.Memberships.objects.filter(user_id=user_id,company_id=company_id).first()
    if member.role != comp_models.Memberships.Roles.User:
        return False
    video = comp_models.Video(member=member,link=link)
    video.save()
    return video

    

def get_user_video_history(member_id):
    member = comp_models.Memberships.objects.filter(pk=member_id).first()
    return comp_models.Video.objects.all().filter(member=member).values_list()


def create_company_by_user(user_id, **company_data):

    new_company = comp_models.Companies.objects.create(**company_data)

    member = comp_models.Memberships.objects.create(
        user_id=user_id, 
        company=new_company, 
        role=comp_models.Memberships.Roles.SuperAdmin
    )
    return new_company, member


