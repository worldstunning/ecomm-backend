from rest_framework import serializers
from .models import Product, CartItem, Category, Address, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source='product'
    )
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']
        read_only_fields = ['user']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product= ProductSerializer()
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), write_only=True, source='address'
    )
    class Meta:
        model = Order
        fields = ['id', 'user', 'address_id', 'created_at', 'paid', 'items']
        read_only_fields = ['user', 'created_at', 'paid']
    
    def create(self, validated_data):
        user = self.context['request'].user
        address= validated_data['address']
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            raise serializers.ValidationError('Cart is Empty')
    
        order = Order.objects.create(user=user, address=address)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product= item.product,
                quantity= item.quantity,
                price= item.product.price,
            )
            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()
        return order