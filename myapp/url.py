from django.urls import path
from .views import qr_generator_scanner

urlpatterns = [
    path("", qr_generator_scanner, name="qr_combined"),
]
