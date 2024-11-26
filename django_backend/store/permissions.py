from rest_framework import permissions
from . import models

class IsOrderOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Standard method signature: (request, view, obj)
        # Modification: Use 'order_pk' from view.kwargs to fetch the Order object and check ownership
        # This allows us to apply the permission at the class level for actions like retrieve, update, and delete
        order_pk = view.kwargs.get('order_pk')
        if order_pk:
            # Fetch the order object
            order = models.Order.objects.get(id=order_pk)
            # Ensure the user is the owner of the order
            return order.user == request.user
        return False