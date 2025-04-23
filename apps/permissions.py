from rest_framework.permissions import BasePermission

from apps.models import User


class IsSellerPermission(BasePermission):
    message="You are not customer"
    def has_permission(self, request, view):
        return request.user.role == User.Roles.seller

class IsCustomerPermission(BasePermission):
    message="You are not seller"
    def has_permission(self, request, view):
        return request.user.role == User.Roles.customer
