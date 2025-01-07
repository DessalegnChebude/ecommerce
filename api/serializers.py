from rest_framework import serializers 
from products.models import Product, Category, ProductImage
from orders.models import Order
from reviews.models import Review
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
        # Override the create method to hash the password.
        password = validated_data.pop('password') # Remove password from the validated data
        user = User(**validated_data)
        user.is_active = True  # this will Ensure the account is active
        user.set_password(password) # Hash the password
        user.save()
        return user
    
    def update(self, instance, validated_data):
    # Override the update method to hash the password if it's updated.
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']
        
        # To make sure rating value is b/n 1 and 5
        def validate_rating(self, value):
            if value < 1 or value > 5:
                raise serializers.ValidationError("Rating must be between 1 and 5.")
            return value
                
class ProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImage
#         fields = ['id', 'image', 'uploaded_at']
    # Include product ID explicitly in the serialized output
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), 
        source='product',  # Maps to the Product model
        write_only=False   # Allows both reading and writing
    )
    class Meta:
        model = ProductImage
        fields = ['id', 'product_id', 'image', 'uploaded_at']  # Include product_id in the fields
            

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)  # Include the reviews in the product detail
    images = ProductImageSerializer(many=True, read_only=True)  # Read-only field for retrieving images


    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'stock_quantity', 'reviews','image_url', 'created_at', 'updated_at', 'created_by','images']
        
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive value.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")
        
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        
