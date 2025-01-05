from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

ORDER_STATUS = (
    ("pending", "pending"),
    ("completed", "completed"),
    ("delivered", "delivered")
)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='orders')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    destination_adress = models.CharField(max_length=255, null=True)
    phone_number = PhoneNumberField(unique=True, help_text="Enter phone number with country code.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200, choices=ORDER_STATUS, default="pending")