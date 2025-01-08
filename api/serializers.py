from rest_framework import serializers 
from products.models import Product, Category, ProductImage, Discount
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
    discounted_price = serializers.ReadOnlyField() # This field is used to compute the discount on products

    class Meta:
        model = Product
        # fields = "__all__"
        fields = ['id', 'name', 'description', 'price', 'discounted_price', 'category', 'stock_quantity', 'reviews','image_url', 'created_at', 'updated_at', 'created_by','images']
        
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive value.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value
    
    def get_discounted_price(self, obj):
        """Calculate discounted_price dynamically."""
        discount = obj.discounts.order_by('-discount_percentage').first()
        if discount:
            return obj.price * (1 - discount.discount_percentage / 100)
        return obj.price
    
    
class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'product', 'discount_percentage', 'start_date', 'end_date']
        
    def create(self, validated_data):
        discount = super().create(validated_data)
        discount.product.apply_discount()  # Apply discount after creation
        return discount

    def update(self, instance, validated_data):
        discount = super().update(instance, validated_data)
        discount.product.apply_discount()  # Apply discount after update
        return discount
        
# Validation used to Prevent Overlapping Discounts: Ensure a product cannot have overlapping discounts.
    def validate(self, data):
        product = data['product']
        start_date = data['start_date']
        end_date = data['end_date']

        if Discount.objects.filter(
            product=product,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists():
            raise serializers.ValidationError("Overlapping discounts are not allowed.")
        return data
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")
        
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        
