from rest_framework import permissions

from .models import Membership


class BaseCompanyRolePermissions(permissions.BasePermission):
    roles = []
    def has_permission(self, request, view):
        company_id = request.data.get('company_id') or view.kwargs.get('company_id')
        if not company_id: # добавить проверку на авторизованность
            return False
        
        return Membership.objects.filter(
            user_id =request.user.id,
            company_id=company_id,
            is_active=True,
            role__in=self.roles
        ).exists()
    

class IsSuperAdmin(BaseCompanyRolePermissions):
    roles=[Membership.Roles.SuperAdmin]

class IsAdmin(BaseCompanyRolePermissions):
    roles=[Membership.Roles.Admin]

class IsUser(BaseCompanyRolePermissions):
    roles=[Membership.Roles.User]

class IsAny(BaseCompanyRolePermissions):
    roles=[Membership.Roles.User, Membership.Roles.Admin, Membership.Roles.SuperAdmin]