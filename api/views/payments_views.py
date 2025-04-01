from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from api.utils.mpesa_client import MpesaClient
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.utils.permissions import IsStaff
from payments.models import MpesaTransaction
from rest_framework import generics, status
from api.serializers.payments_serializers import MpesaTransactionSerializer, PaymentsRequestPayLoadSerializer
from rest_framework import filters
from api.utils import helpers
from django.views.decorators.csrf import csrf_exempt


class MpesaSTKPushView(APIView):
    permission_classes = [IsStaff]

    def post(self, request):

        serializer = PaymentsRequestPayLoadSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        requesting_user = request.user
        print(f"Requesting User:{requesting_user}")

        phone_number = serializer.validated_data["phone_number"]
        amount = serializer.validated_data["amount"]
        account_reference = helpers.generate_reference()
        member_id = serializer.validated_data["member"]
        
        print(f"Member: {member_id}" )

        payment_method = serializer.validated_data["payment_method"]
        print(f"Payment Method: {payment_method}" )
        
        transaction_desc = serializer.validated_data["description"]

        if not transaction_desc:
            transaction_desc = "Payment for services"

        match payment_method:
            case "M-Pesa":
                print("Processing Mpesa Payments")
                mpesa = MpesaClient()
                response = mpesa.stk_push( phone_number, amount, account_reference, transaction_desc )

                if "error" in response:
                    return Response(response, status=400)

                response_code = response.get("ResponseCode")
                checkout_request_id = response.get("CheckoutRequestID")
                merchant_request_id = response.get("MerchantRequestID")
                if response_code == "0":
                    MpesaTransaction.objects.create(
                        merchant_request_id=merchant_request_id,
                        checkout_request_id=checkout_request_id,
                        reference=account_reference,
                        phone_number=phone_number,
                        amount=amount,
                        description = transaction_desc,
                    )

                return Response(response, status=200)
            
            case "Cash":
                print("Processing Cash Payments")
                return Response({"message": "Cash Payment Confirmed"}, status=status.HTTP_200_OK)
            case _:
                print("Unknown Payments method")
                return Response({"error": "Invalid Payment Method", "message": "Payment Method not recognized"}, status=status.HTTP_400_BAD_REQUEST)




@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def mpesa_callback(request):
    data = request.data
    print("M-Pesa Callback Received:", data)  # Debugging

    try:
        callback_data = data.get("Body", {}).get("stkCallback", {})
        checkout_request_id = callback_data.get("CheckoutRequestID")
        result_code = callback_data.get("ResultCode")
        result_desc = callback_data.get("ResultDesc")

        # Get transaction from db
        transaction = transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)

        transaction.result_code = result_code
        transaction.result_desc = result_desc

        if result_code == 0:
            print("Processing successful payment")

            transaction.status = "Completed"

            metadata = callback_data.get("CallbackMetadata", {}).get("Item", [])
            for item in metadata:
                if item["Name"] == "Amount":
                    transaction.amount = item["Value"]
                elif item["Name"] == "MpesaReceiptNumber":
                    transaction.mpesa_receipt_number = item["Value"]
                elif item["Name"] == "TransactionDate":
                    transaction.transaction_date = item["Value"]
                elif item["Name"] == "PhoneNumber":
                    transaction.phone_number = str(item["Value"])
            transaction.save()
            print("Transaction saved as Completed")

            transaction_data = MpesaTransactionSerializer(transaction).data

            return Response({"transaction_details": transaction_data}, status=200)
        else:
            print("Processing failed payment")
            transaction.status = "Failed"
            transaction.save()

            return Response({"error": "Payment failed", "message": result_desc}, status=400)
    except MpesaTransaction.DoesNotExist:
        print(f"Transaction with CheckoutRequestID {checkout_request_id} not found")
        return Response({"error": "Transaction not found", "message": "No such transaction"}, status=400)

    except Exception as e:
        print("Error processing M-Pesa callback:", str(e))
        return Response({"error": "Invalid callback data"}, status=400)


class FetchMpesaTransactionView(generics.ListAPIView):

    queryset = MpesaTransaction.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = MpesaTransactionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["id","phone_number", "transaction_date", "mpesa_receipt_number", "checkout_request_id"]
