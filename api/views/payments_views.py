from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.utils.mpesa_client import MpesaClient
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
    # Process callback data (store in DB, update order status, etc.)
    print("M-Pesa Callback Received:", data)

    return Response({"message": "Callback received"}, status=200)