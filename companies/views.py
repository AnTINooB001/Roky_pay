from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
import json

from . import models as comp_models

from .services import get_company_by_name, get_or_create_company_member, get_video_to_admin_review, \
    set_video_solution, create_and_save_user_video_to_db ,get_user_video_history, create_and_save_company_to_db_by_user_id
from .serializers import CompanySerializer

class CompanyListApiView(generics.ListCreateAPIView):
    queryset=comp_models.Companies.objects.all()
    serializer_class=CompanySerializer

    def perform_create(self, serializer):
        new_company = serializer.save()
        


@csrf_exempt
def set_video_solution_view(request):
    if request.method == "PATCH":
        body_json = json.loads(request.body)
        admin_id = body_json.get('admin_id')
        solution = body_json.get('solution')
        res = set_video_solution(admin_id,solution)
    return JsonResponse({'result': res})


def get_video_to_admin_review_view(request):
    if request.method == 'GET':
        json_body = json.loads(request.body)
        admin_id = json_body.get('admin_id')
        video = get_video_to_admin_review(admin_id)
        if video is None:
            return JsonResponse({'result' : None})
        return JsonResponse({'result': {'video' : {'video_id': video.pk, 'video_link': video.link, 'video_member': video.member.user.username}}})


@csrf_exempt
@login_required
def home_view(request, company_name):
    company = get_company_by_name(company_name)
    member, _ = get_or_create_company_member(company=company,user=request.user)
# -------------------------------- SUPER USER --------------------------------------
    if member.role == 'Super Admin':
        return render(request, 'companies/superAdmin.html', {'member': member})
# -------------------------------- ADMIN --------------------------------------
    elif member.role == 'Admin':
        context = {'member': member,}
        return render(request, 'companies/admin.html', context)
# -------------------------------- USER --------------------------------------
    elif member.role == 'User':
        history = get_user_video_history(member.pk)
        return render(request, 'companies/user.html',{'history':history, 'member': member})
    

@csrf_exempt
def create_video_by_user_view(request):
    if request.method == 'POST':
        try:
            json_body = json.loads(request.body)
            member_id = json_body.get('member_id')
            link = json_body.get('link')
            create_and_save_user_video_to_db(link,member_id)
        except Exception as e:
            return JsonResponse({'result': 'error', 'error': f'e'})
        else:
            return JsonResponse({'result': 'ok'})
        
@csrf_exempt
def create_company_by_user_view(request):
    if request.method == "POST":
        json_body = json.loads(request.body)
        name = json_body.get('name')
        description = json_body.get('description')
        if create_and_save_company_to_db_by_user_id(request.user.pk, name, description):
            return JsonResponse({'result' : 'ok'})
        else:
            return JsonResponse({'result':'error'})
    return JsonResponse({'lol':'lol'})