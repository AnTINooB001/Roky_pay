from companies import models as comp_models
from django.contrib.auth import get_user_model
from typing import Optional 


def get_company_by_name(name: str):
    return comp_models.Companies.objects.get(name=name)


def get_or_create_company_member(company, user):
    return comp_models.Memberships.objects.get_or_create(user=user,company=company)


def get_video_to_admin_review(member_id) -> Optional[comp_models.Video]:
    """Возвращает video для оценки admin'ом или
                  None если видео для оценки отсутствует"""
    admin_member = comp_models.Memberships.objects.filter(pk=member_id).first()
    if admin_member is None or admin_member.role != comp_models.Memberships.Roles.Admin:
        return None
    solutions = comp_models.Video.Solution
    video = comp_models.Video.objects.filter(admin=admin_member).filter(solution=solutions.Wait).first()
    if video is None:
        video = comp_models.Video.objects.filter(admin=None).first()
        if video is None:
            return None
        video.admin = admin_member
        video.save()
    return video


def set_video_solution(admin_id,solution) -> bool:
    try:
        
        video = comp_models.Video.objects.filter(admin__pk=admin_id).get(solution=comp_models.Video.Solution.Wait)
        video.solution = solution
        video.save()
    except Exception as e:
        print(f'error: {e} in setting solution to video, soltion - {solution}, admin_id - {admin_id}')
        return False
    else:
        return True


def create_and_save_user_video_to_db(link, member_id):
    try:
        member = comp_models.Memberships.objects.filter(pk=member_id).first()
        video_record = comp_models.Video(member=member,link=link)
        video_record.save()
    except Exception as e:
        print(f'error in creating and saving video - {e}')
        return False
    else:
        return True
    

def get_user_video_history(member_id):
    member = comp_models.Memberships.objects.filter(pk=member_id).first()
    return comp_models.Video.objects.all().filter(member=member).values_list()


def create_and_save_company_to_db_by_user_id(user_id, name, description):
    try:
        new_company = comp_models.Companies(name=name, description=description)
        new_company.save()

        roles = comp_models.Memberships.Roles
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=user_id)
        member = comp_models.Memberships(user=user, company=new_company, role=roles.SuperAdmin)
        member.save()
    except Exception as e:
        print(f'error while creating company {e}')
        return False
    else:
        return True
    
    
def get_all_companies():
    return comp_models.Companies.objects.all()