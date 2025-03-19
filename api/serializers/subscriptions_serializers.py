from rest_framework.serializers import ModelSerializer
from subscriptions.models import Plan, Subscription
from users.models import CustomUser


class PlanSerializer(ModelSerializer):
  class Meta:
    model = Plan
    fields = "__all__"
  
class MemberSerailizer(ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ["id", "username", "first_name", "last_name", "email", "phone_number"]
  

class SubscriptionSerializer(ModelSerializer):
  plan = PlanSerializer()
  member = MemberSerailizer()
  
  class Meta:
    model = Subscription
    fields = ["member", "plan", "start_date", "end_date", "status", "created_at", "updated_at"]
  
  
    