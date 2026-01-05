from django.http import request, response
from django.shortcuts import render
from companies import models as comp_models

class CheckUserStatusMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self, request):
        paths = request.path.split('/')
        req_company = comp_models.Companies.objects.filter(name__in=paths).first()
        if req_company is not None:
            member = comp_models.Memberships.objects.filter(user=request.user).filter(company=req_company).first()

            if member is not None and member.status == comp_models.Memberships.Status.Banned:
                return render(request, 'general/banned.html')
        
        response = self.get_response(request)
        
        return response
