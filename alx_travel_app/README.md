# 🧾 Chapa Payment Integration — alx_travel_app_0x02

This Django project integrates with the **Chapa Payment API** to handle secure online payments for travel bookings. It supports payment initiation, verification, transaction status updates, and email confirmation via Celery background tasks.

---

## 🚀 Features

- Secure payment integration with [Chapa](https://developer.chapa.co/)
- API-based booking and transaction workflow
- Payment verification using transaction reference
- Email confirmation on successful payment using Celery and Redis
- Testable in Chapa sandbox mode

---

## ⚙️ How It Works

1. A user creates a booking and initiates payment.
2. A Payment object is created with status "Pending" and a unique booking_reference.
3. A POST request is sent to Chapa’s /transaction/initialize endpoint with booking details.
4. Chapa returns a checkout_url which is shared with the user.
5. After completing the payment, Chapa redirects to a verification endpoint.
6. The server verifies the transaction via Chapa’s /transaction/verify/<reference> endpoint.
7. Payment status is updated to "Completed" or "Failed", and a confirmation email is sent.

---

## 📡 API Endpoints

| Method | Endpoint                                 | Description                         |
|--------|------------------------------------------|-------------------------------------|
| POST   | /api/initiate-payment/                 | Initiates a payment transaction     |
| GET    | /api/verify-payment/<booking_reference>/ | Verifies the payment and updates status |

---

## 🔧 Environment Setup

Create a .env file at the root of your project with the following:

env
CHAPA_SECRET_KEY=CHAPUBK_TEST-jRJkkrE7PgwCCiqVv9KN1BgDcHzyKfv4
EMAIL_HOST_USER=youremail@example.com
EMAIL_HOST_PASSWORD=your_app_password

## ⚙️ Celery & Redis Setup
Install dependencies:


pip install requests python-dotenv celery redis django-celery-results
Run Redis server (in a separate terminal):


redis-server
Start the Celery worker:


celery -A alx_travel_app worker -l info
## 📦 Example API Payloads
Initiate Payment
json

{
  "name": "Test User",
  "email": "test@example.com",
  "amount": "100.00"
}
Returns a checkout_url from Chapa.

User completes payment via the provided link.

Chapa redirects to /api/verify-payment/<booking_reference>/.

🧪 Sandbox Testing
This project uses Chapa’s sandbox public key:
CHAPUBK_TEST-jRJkkrE7PgwCCiqVv9KN1BgDcHzyKfv4

Payments are simulated.

Check database or logs for payment status after verification.

Confirm email delivery via terminal log or SMTP inbox.

## 📁 Project Structure

alx_travel_app_0x02/
├── alx_travel_app/
│   ├── settings.py
│   └── urls.py
├── listings/
│   ├── models.py       # Payment model
│   ├── views.py        # Payment initiate & verify logic
│   ├── tasks.py        # Celery email confirmation task
│   ├── urls.py
│   └── templates/emails/payment_confirmation.html
├── .env
├── README.md
└── requirements.txt


## 🚫 .gitignore (Recommended)

-#Python/Django
__pycache__/
*.pyc
*.sqlite3
media/
staticfiles/

#Environment
.env

#IDEs
.vscode/
.idea/

#Celery/Redis
celerybeat-schedule
*.pid
## 🤝 Acknowledgments
This project was developed as part of the ALX Software Engineering Program.
Powered by Chapa — the leading payment gateway in Ethiopia.

---
