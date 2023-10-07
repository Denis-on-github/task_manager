from rest_access_policy import AccessPolicy


class IsStaffOrReadOnly(AccessPolicy):
    def get_permissions(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user and request.user.is_staff

    def has_permission(self, request, view):
        return self.get_permissions(request, view, None)

    def has_object_permission(self, request, view, obj):
        return self.get_permissions(request, view, obj)
