from rest_framework import serializers
from payments.models import MpesaTransaction, Payment
from phonenumber_field.serializerfields import PhoneNumberField
from api.utils import helpers
from decimal import Decimal, InvalidOperation
from rest_framework import exceptions

class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
        fields = "__all__"

class PaymentsRequestPayLoadSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)  # Only for M-Pesa
    reference = serializers.CharField(required=False, allow_blank=True)  # Only for M-Pesa
    description = serializers.CharField(required=False, allow_blank=True)  # Only for M-Pesa
    amount = serializers.CharField()

    class Meta:
        model = Payment
        fields = [
            "member",
            "amount",
            "payment_method",
            "plan",
            "phone_number",
            "reference",
            "description"
        ]

    def validate(self, data):
        payment_method = data.get("payment_method")
        plan = data.get("plan")
        amount = data.get("amount")

        # Ensure amount is provided
        if not amount:
            raise serializers.ValidationError({"amount": "Amount is Required"})

        # Convert to Decimal and check minimum value
        try:
            amount = Decimal(amount)
            if amount < 1:
                raise serializers.ValidationError({"amount": "Amount is Required"})
        except (InvalidOperation, ValueError):
            raise serializers.ValidationError({"amount": "Must be a valid number"})

        # data["amount"] = str(amount) Not necessary

        if not plan:
            raise serializers.ValidationError({"plan": "You have to choose a plan"})

        if payment_method == "M-Pesa":
            if not data.get("phone_number"):
                raise serializers.ValidationError({"phone_number": "Phone number is required for M-Pesa payments."})
            if not data.get("description"):
                raise serializers.ValidationError({"account_reference": "Account reference is required for M-Pesa payments."})
            if not data.get("description"):
                raise serializers.ValidationError({"transaction_description": "Transaction description is required for M-Pesa payments."})

        if payment_method == "Cash": ...
            # Remove unnecessary fields for cash payments
            # data.pop("phone_number", None)
            # data.pop("account_reference", None)
            # data.pop("transaction_description", None)

        return data
