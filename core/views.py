from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Product, CartItem, Category, Address, Order, OrderItem
from .serializers import ProductSerializer, CartItemSerializer, CategorySerializer, AddressSerializer, OrderSerializer
from rest_framework .permissions import IsAuthenticated
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config

stripe.api_key = config('STRIPE_SECRET_KEY')

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        existing= CartItem.objects.filter(
            user=self.request.user, product=serializer.validated_data['product']
        ).first()
        if existing:
            existing.quantity += serializer.validated_data['quantity']
            existing.save()
        else:
            serializer.save(user=self.request.user)

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StripeCheckoutView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id') 
        order = Order.objects.get(id=order_id, user=request.user)

        line_items = []
        for item in order.items.all():
            line_items.append({
                'price_data':{
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.price *100)
                },
                'quantity': item.quantity
            })

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:3000/cancel',
            client_reference_id=str(order.id),
            customer_email=request.user.email,
        ) 

        return Response({'checkout_url':session.url})