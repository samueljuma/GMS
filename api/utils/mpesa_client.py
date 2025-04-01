import requests
import datetime
import base64
from django.conf import settings


class MpesaClient:
    def __init__(self):
        self.base_url = "https://sandbox.safaricom.co.ke" if settings.MPESA_ENV == "sandbox" else "https://api.safaricom.co.ke"

    def get_access_token(self):
        # url = settings.ACCESS_TOKEN_URL

        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

        # Make the request with Basic Auth
        response = requests.get(url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))

        print("Access Token Response:", response.status_code, response.text)  # Debugging

        if response.status_code != 200:
            raise Exception(f"Failed to get access token: {response.status_code}, {response.text}")

        try:
            return response.json().get("access_token")
        except requests.exceptions.JSONDecodeError:
            raise Exception(f"Invalid JSON response: {response.text}")

    def generate_password(self, timestamp):
        """Generates Mpesa API password using the provided shortcode and passkey"""
        password_str = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
        password_bytes = password_str.encode("utf-8")  # Convert to bytes
        return base64.b64encode(password_bytes).decode("utf-8")  # Encode and decode to string

    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        try:
            access_token = self.get_access_token()

            if not access_token:
                return {"error": "Failed to get access token"}

            # url = settings.STK_PUSH_URL

            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {
                "Authorization": f"Bearer {access_token}",
            }

            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            print("timestamp:", timestamp)

            password = self.generate_password(timestamp=timestamp)
            print("Generated Password:", password)

            payload = {
                "BusinessShortCode": settings.MPESA_SHORTCODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": settings.MPESA_SHORTCODE,
                "PhoneNumber": phone_number,
                "CallBackURL": "https://cbea-41-220-235-155.ngrok-free.app/api/mpesa/callback/",
                "AccountReference": account_reference,
                "TransactionDesc": transaction_desc,
            }

            print(f"payload : {payload}")

            response = requests.post(url, json=payload, headers=headers)

            print("STK Push Response:", response.status_code, response.text) 

            if response.status_code != 200:
                return {"error": f"STK Push failed: {response.status_code}, {response.text}"}

            return response.json()
        except Exception as e:
            return {"error": str(e)}
