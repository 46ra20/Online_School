from rest_framework import permissions
from account.models import UserRegistrarionModel


class TeacherCanUpdateAndDeleteCourse(permissions.BasePermission):
    def has_permission(self, request, view):
        
        try:
            is_teacher = UserRegistrarionModel.objects.get(user=request.user)
            print(is_teacher.account_type)
        except(UserRegistrarionModel.DoesNotExist):
            is_teacher=None
        
        if is_teacher is not None and is_teacher.account_type=='Teacher':
            print('Yes')
            return True
        # return super().has_permission(request, view)