from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.utils.mpesa_client import MpesaClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from payments.models import MpesaTransaction
from rest_framework import generics
from api.serializers.payments_serializers import MpesaTransactionSerializer
from rest_framework import filters


class MpesaSTKPushView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get("phone_number")
        amount = request.data.get("amount")
        account_reference = "Test Payment"
        transaction_desc = "Payment for services"

        if not phone_number or not amount:
            return Response(
                {"error": "Phone number and amount are required"}, status=400
            )

        mpesa = MpesaClient()
        response = mpesa.stk_push( phone_number, amount, account_reference, transaction_desc )

        if "error" in response:
            return Response(response, status=400)

        return Response(response, status=200)


@api_view(["POST"])
def mpesa_callback(request):
    data = request.data
    print("M-Pesa Callback Received:", data)  # Debugging

    try:
        callback_data = data.get("Body", {}).get("stkCallback", {})

        merchant_request_id = callback_data.get("MerchantRequestID")
        checkout_request_id = callback_data.get("CheckoutRequestID")
        result_code = callback_data.get("ResultCode")
        result_desc = callback_data.get("ResultDesc")

        # Extract optional fields if present
        amount = None
        mpesa_receipt_number = None
        transaction_date = None
        phone_number = None

        if result_code == 0:
            metadata = callback_data.get("CallbackMetadata", {}).get("Item", [])
            for item in metadata:
                if item["Name"] == "Amount":
                    amount = item["Value"]
                elif item["Name"] == "MpesaReceiptNumber":
                    mpesa_receipt_number = item["Value"]
                elif item["Name"] == "TransactionDate":
                    transaction_date = item["Value"]
                elif item["Name"] == "PhoneNumber":
                    phone_number = item["Value"]

        # Save transaction to database
        transaction = MpesaTransaction.objects.create(
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
            result_code=result_code,
            result_desc=result_desc,
            amount=amount,
            mpesa_receipt_number=mpesa_receipt_number,
            transaction_date=transaction_date,
            phone_number=phone_number,
        )
        
        # Serialize transaction details
        transaction_data = MpesaTransactionSerializer(transaction).data

        # Return appropriate response code based on success or failure
        if result_code == 0:
            return Response({"transaction_details": transaction_data}, status=200)  # ✅ Success
        else:
            return Response({"error": "Payment failed", "message": result_desc}, status=400) 

    except Exception as e:
        print("Error processing M-Pesa callback:", str(e))
        return Response({"error": "Invalid callback data"}, status=400)


class FetchMpesaTransactionView(generics.ListAPIView):

    queryset = MpesaTransaction.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = MpesaTransactionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["phone_number", "transaction_date", "mpesa_receipt_number"]
