import os
import uuid
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Payment
from .tasks import send_payment_confirmation_email
from dotenv import load_dotenv

load_dotenv()

CHAPA_API = "https://api.chapa.co/v1"
CHAPA_SECRET = os.getenv("CHAPA_SECRET_KEY")

@api_view(["POST"])
def initiate_payment(request):
    reference = str(uuid.uuid4())
    amount = request.data.get("amount")
    email = request.data.get("email")
    name = request.data.get("name")

    payload = {
        "amount": amount,
        "currency": "ETB",
        "email": email,
        "first_name": name,
        "tx_ref": reference,
        "callback_url": f"http://localhost:8000/api/verify-payment/{reference}/",
        "return_url": f"http://localhost:8000/payment-success/",
        "customization[title]": "Booking Payment"
    }

    headers = {
        "Authorization": f"Bearer {CHAPA_SECRET}"
    }

    r = requests.post(f"{CHAPA_API}/transaction/initialize", json=payload, headers=headers)
    data = r.json()

    if data["status"] == "success":
        Payment.objects.create(booking_reference=reference, amount=amount, email=email)
        return Response({"checkout_url": data["data"]["checkout_url"], "reference": reference})
    return Response({"error": data}, status=400)

@api_view(["GET"])
def verify_payment(request, reference):
    headers = {
        "Authorization": f"Bearer {CHAPA_SECRET}"
    }
    url = f"{CHAPA_API}/transaction/verify/{reference}"
    r = requests.get(url, headers=headers)
    result = r.json()

    try:
        payment = Payment.objects.get(booking_reference=reference)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)

    if result["status"] == "success" and result["data"]["status"] == "success":
        payment.status = "Completed"
        payment.transaction_id = result["data"]["tx_ref"]
        payment.save()
        send_payment_confirmation_email.delay(payment.email, reference)
        return Response({"message": "Payment verified."})
    else:
        payment.status = "Failed"
        payment.save()
        return Response({"message": "Payment failed."})

