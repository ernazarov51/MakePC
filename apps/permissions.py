from rest_framework.permissions import BasePermission

from apps.models import User


class IsSellerPermission(BasePermission):
    message="You are not seller"
    def has_permission(self, request, view):
        return request.user.role == User.Roles.seller

class IsCustomerPermission(BasePermission):
    message="You are not customer"
    def has_permission(self, request, view):
        return request.user.role == User.Roles.customer

class IsAdminPermission(BasePermission):
    message="You are not admin"
    def has_permission(self, request, view):

        email=request.data['email']
        user=User.objects.filter(email=email)
        if user.exists():
            return user.first().is_superuser
        self.message="Admin with this email does not exists"
