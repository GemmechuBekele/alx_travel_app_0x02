# Chapa Payment Integration

This project integrates the Chapa API with a Django booking system.

## How It Works

1. User initiates a payment.
2. System creates a Payment object with "Pending" status.
3. Chapa redirects to the verify endpoint.
4. Payment status is verified and updated to "Completed" or "Failed".
5. A confirmation email is sent using Celery.

## API Endpoints

- `POST /api/initiate-payment/`
- `GET /api/verify-payment/<booking_reference>/`

## Environment Variables
- CHAPA_SECRET_KEY=CHAPUBK_TEST-...
- EMAIL_HOST_USER=youremail@example.com
- EMAIL_HOST_PASSWORD=your_app_password

## Dependencies

- Celery
- Redis
- requests
