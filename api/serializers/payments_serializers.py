from rest_framework import serializers
from payments.models import MpesaTransaction
from phonenumber_field.serializerfields import PhoneNumberField
from api.utils import helpers

class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
        fields = "__all__"