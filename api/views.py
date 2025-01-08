from django.shortcuts import render
from .serializers import DiscountSerializer, ProductImageSerializer, UserSerializer, ProductSerializer, CategorySerializer, OrderSerializer, ReviewSerializer
from reviews.models import Review
from products.models import Discount, Product, Category, ProductImage
from orders.models import Order
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import  IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import ValidationError


User = get_user_model()

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'price', 'stock_quantity']
    search_fields = ['name', 'category__name']
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Optionally apply filtering logic for discounted products
        return queryset

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Override to check stock before creating an order."""
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        if product.stock_quantity < quantity:
            return Response(
                {"error": f"Not enough stock available for {product.name}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Reduce stock within a transaction to ensure atomicity
        with transaction.atomic():
            product.stock_quantity -= quantity
            product.save()
            serializer.save()
            
    def perform_update(self, serializer):
        old_order = self.get_object()
        new_quantity = serializer.validated_data['quantity']
        product = serializer.validated_data['product']
        try:
            with transaction.atomic():
                # Restore the old stock
                product.stock_quantity += old_order.quantity

                # Check stock for the new quantity
                if product.stock_quantity < new_quantity:
                    raise ValidationError(
                        {"error": f"Not enough stock available for {product.name}."}
                    )

                # Deduct the new quantity
                product.stock_quantity -= new_quantity
                product.save()

                # Save the updated order
                serializer.save()
        except:
            raise ValidationError(
                {"error": f"Not enough stock available for {product.name}."})
            
    def perform_destroy(self, instance):
        try:
            with transaction.atomic():
                # Restore the stock
                product = instance.product
                product.stock_quantity += instance.quantity
                product.save()

                # Delete the order
                instance.delete()
        except:
            print({"error": f"unable to delete {product.name}."})
            
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user) 
        
class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    
class DiscountViewSet(ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer