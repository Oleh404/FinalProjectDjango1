from rest_framework import permissions

class IsBookingOwnerOrLandlord(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        if request.user == obj.rental_property.owner:
            return True
        return False


class IsLandlordOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.rental_property.owner
