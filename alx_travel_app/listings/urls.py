from django.urls import path
from .views import initiate_payment, verify_payment

urlpatterns = [
    path("initiate-payment/", initiate_payment),
    path("verify-payment/<str:reference>/", verify_payment),
]
