from rest_framework import serializers
from subscriptions.models import Plan, Subscription
from users.models import CustomUser
from api.serializers.payments_serializers import PaymentSerializer


class PlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = Plan
    fields = "__all__"
  
class MemberSerailizer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ["id", "username", "first_name", "last_name", "email", "phone_number"]
  

class SubscriptionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Subscription
    fields = "__all__"
  
  
