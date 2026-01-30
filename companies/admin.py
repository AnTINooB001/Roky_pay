from django.contrib import admin
from . import models as comp_models
from user_app import models as user_models


@admin.register(comp_models.Companies)
class ComplaniesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.system_admin:
            return qs
        roles = comp_models.Memberships.Roles
        member = comp_models.Memberships.objects.filter(user=request.user).filter(role=roles.SuperAdmin)
        if(member.count() == 0):
            return qs.none()
        qs = qs.filter(memberships__in=member)
        return qs


@admin.register(comp_models.Memberships)
class CompaniesMembersAdmin(admin.ModelAdmin):
    list_display = ('id','user','role', 'status','company')
    list_editable = ('role','status')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.system_admin:
            return qs.exclude(user=request.user)
        roles = comp_models.Memberships.Roles
        super_admin_records = comp_models.Memberships.objects.filter(user=request.user).filter(role=roles.SuperAdmin)
        companies = [super_admin_record.company for super_admin_record in super_admin_records]
        qs = qs.filter(company__in=companies).exclude(user=request.user)
        return qs
    
@admin.register(comp_models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'link', 'date', 'solution','admin')
    list_editable = ['solution',]