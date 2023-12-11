from rest_framework.permissions import BasePermission


class IsUserCreator(BasePermission):
    """
    Класс для запрета модерирование не своих привычек
    """

    def has_permission(self, request, view):
        if view.get_object().user == request.user:
            return True
        return False


class IsPublicHabit(BasePermission):
    """
    Если привычка публичная, то ее можно просмотреть
    """
    def has_permission(self, request, view):
        if view.get_object().is_public:
            return True
        return False
