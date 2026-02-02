from rest_framework import permissions

from .models import Memberships

class BaseCompanyRolePermissions(permissions.BasePermission):
    roles = []
    def has_permission(self, request, view):
        company_id = request.data.get('company_id') or view.kwargs.get('company_id')
        print(f'user_id - {request.user.id}, company_id - {company_id}')
        if not company_id:
            return False
        
        return Memberships.objects.filter(
            user_id =request.user.id,
            company_id=company_id,
            is_active=True,
            role__in=self.roles
        ).exists()
    

class IsSuperAdmin(BaseCompanyRolePermissions):
    roles=[Memberships.Roles.SuperAdmin]

class IsAdmin(BaseCompanyRolePermissions):
    roles=[Memberships.Roles.Admin]

class IsUser(BaseCompanyRolePermissions):
    roles=[Memberships.Roles.User]

class IsAny(BaseCompanyRolePermissions):
    roles=[Memberships.Roles.User, Memberships.Roles.Admin, Memberships.Roles.SuperAdmin]