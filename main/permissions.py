from rest_access_policy import AccessPolicy


class IsStaffOrReadOnly(AccessPolicy):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_staff
        return True
