from django.db import models
from django.dispatch import receiver
from products.models import Product
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

User = get_user_model()

ORDER_STATUS = (
    ("pending", "pending"),
    ("completed", "completed"),
    ("delivered", "delivered")
)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='orders')
    quantity = models.PositiveBigIntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    destination_adress = models.CharField(max_length=255, null=True)
    phone_number = PhoneNumberField(help_text="Enter phone number with country code.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200, choices=ORDER_STATUS, default="pending"),
    
    def __str__(self):
        return f"Order of {self.quantity} {self.product.name}"
    
    
@receiver(post_save, sender=Order)
def reduce_stock(sender, instance, created, **kwargs):
    if created:  # Only reduce stock for new orders
        product = instance.product

    # Ensure stock is sufficient
    if product.stock_quantity >= instance.quantity:
        with transaction.atomic():  # Ensure atomicity to prevent race conditions
            product.stock_quantity -= instance.quantity
            product.save()
    else:
        raise ValueError(f"Not enough stock available for {product.name}.")
