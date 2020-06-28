from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    message = "Only SuperAdmin has permisison for it."
    
    def has_permission(self, request, view):
        try:
            if request.user.account_type == 'S':
                return True
            return False
        except Exception as e:
            print("error--->", str(e))
            return False

class OnlyAdmin(permissions.BasePermission):
    message = "Admin and SuperAdmin has permisison for it."
    
    def has_permission(self, request, view):
        try:
            if request.user.account_type == 'A' or request.user.account_type == 'S':
                return  True
            return False
        except Exception as e:
            print("error--->", str(e))
            return 


class OnlyUser(permissions.BasePermission):
    message = "Only User has permisison for it."
    
    def has_permission(self, request, view):
        try:
            if request.user.account_type == 'U':
                return  True
            return False
        except Exception as e:
            print("error--->", str(e))
            return 