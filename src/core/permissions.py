from rest_framework import permissions


class HasFunctionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        member = user.member

        required_functions_mapping = getattr(view, "required_functions", {})
        required_functions = required_functions_mapping.get(view.action, [])

        return (member.function in required_functions) or user.is_superuser
