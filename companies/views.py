from django.shortcuts import render
from django.http import HttpResponse, Http404
from companies import models as comp_models
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from . import forms
from videos_app import models as video_models

@login_required
def home(request, company_name):

    try:
        req_company = comp_models.Companies.objects.get(name=company_name)
        
    except(BaseException):
        raise Http404()
    
    try:
        member = comp_models.Memberships.objects.filter(company=req_company.pk).get(user=request.user.pk)

    except(BaseException):
        model = get_user_model()
        user = model.objects.get(id=request.user.pk)
        member = comp_models.Memberships(company=req_company, user=user)
        member.save()

# -------------------------------- SUPER USER --------------------------------------
    if member.role == 'Super Admin':
        return render(request, 'companies/superAdmin.html', {'member': member})
    
# -------------------------------- ADMIN --------------------------------------
    elif member.role == 'Admin':
        context = {'member':member,}
        if request.method == 'POST':
            
            action = request.POST['action']
            type = request.POST['type']
            solutions = video_models.Video.Solution

            if type == 'video':
                video = video_models.Video.objects.filter(admin=member).filter(solution=solutions.Wait).first()
                if video is None:
                    video = video_models.Video.objects.filter(admin=None).first()
                
                if video is None:
                    context['review_video'] = video
                    return render(request, 'companies/admin.html', context)

                video.admin = member

                if(action == 'accept_video' and video):
                    video.solution = solutions.Approved
                    video.save()
                    video = None
                    
                if(action == 'decline_video' and video):
                    video.solution = solutions.Declined
                    video.save()
                    video = None

                context['review_video'] = video

        return render(request, 'companies/admin.html', context)

# -------------------------------- USER --------------------------------------
    elif member.role == 'User':

        form = forms.SendLinkForm()

        if request.method == 'POST':
            form = forms.SendLinkForm(request.POST)
            if form.is_valid():
                link = form.cleaned_data['link']
                video_record = video_models.Video(member=member,link=link)
                video_record.save()
        
        history = video_models.Video.objects.all().filter(member=member).values_list()
        return render(request, 'companies/user.html',{'form':form, 'history':history, 'member':member})
    
    