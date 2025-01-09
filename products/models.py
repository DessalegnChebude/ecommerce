from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.forms import ValidationError
from django.utils.timezone import now

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f"{self.name}"

class Discount(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='discounts')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    def clean(self):
        # Validation logic
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date.")
        super().clean()
    
    def __str__(self):
        return f'{self.discount_percentage}% off {self.product.name}'
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', default=None, null=True)

    def apply_discount(self):
        # Check if there is an active discount
        active_discount = self.discounts.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).first()
        if active_discount:
            self.discounted_price = self.price * (1 - active_discount.discount_percentage / 100)
        else:
            self.discounted_price = None  # No active discount
        self.save()
    
    
    
    def __str__(self):
        return f"{self.name}"
    
# create a productimage class to handle the multiple image upload for a particular product
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/') # Automatically saves to MEDIA_ROOT/product_images/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image for {self.product.name}'