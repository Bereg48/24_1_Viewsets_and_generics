from rest_framework import permissions
from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsModerator(BasePermission):
    """Класс IsModerator наследуется от класса BasePermission и устанавливает доступ пользователю, если он является
    модератором, по средством переопределения метода has_permission"""
    message = 'Вы не являетесь модератором!'

    def has_permission(self, request, view):
        if request.user.roles == UserRoles.MODERATOR:
            return True
        return False


class IsOwner(BasePermission):
    """Класс IsOwner наследуется от класса BasePermission и устанавливает доступ пользователю, если он является
        владельцем создающим объект, по средством переопределения метода has_object_permission"""
    message = 'Вы не являетесь владельцем!'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False


class IsOwnerUpdate(BasePermission):
    """Класс IsOwnerUpdate наследуется от класса BasePermission и устанавливает доступ пользователю, если он является
            владельцем создающим объект, по средством переопределения метода has_permission"""
    def has_permission(self, request, view):
        if request.user == view.get_object().user:
            return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Класс IsOwnerOrReadOnly наследуется от класса BasePermission и устанавливает доступ пользователю, если он является
                владельцем создающим объект, по средством переопределения метода has_object_permission"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
