from api.utils.permissions import IsAdminForPlans
from api.serializers.subscriptions_serializers import PlanSerializer
from rest_framework import viewsets
from subscriptions.models import Plan, Subscription
from django.db.models import ProtectedError
from rest_framework import serializers


class PlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing membership plans.
    - Admins can create, update, and delete plans.
    - Trainers & Members can only view available plans.
    - Guests cannot access.
    """

    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAdminForPlans]

    def perform_destroy(self, instance):
        """Handle deletion errors  on plans that are associated with subscriptions"""
        try:
            instance.delete()
        except ProtectedError:
            raise serializers.ValidationError(
                "Cannot delete this plan because it has subscriptions associated to it."
            )
