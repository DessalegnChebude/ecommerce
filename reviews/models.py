from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
# Create your models here.

User = get_user_model()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField() # Rating should be out of 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'review for {self.product.name} by {self.user.username}'
    
    class Meta:
        ordering = ['-created_at']   # Newest reviews first